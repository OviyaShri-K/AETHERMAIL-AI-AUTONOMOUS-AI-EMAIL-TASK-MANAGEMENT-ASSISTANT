import os
import json
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from app.config import settings

# 1. Pydantic Structured Output Schema for Gemini
class ExtractedTask(BaseModel):
    title: str = Field(description="Clear, imperative action summary for the user")
    description: Optional[str] = Field(None, description="Detailed instructions extracted from email")
    assignee: str = Field(default="user", description="Who is assigned to this task")

class ExtractedDeadline(BaseModel):
    type: Literal["deadline", "event", "meeting", "reminder"] = "deadline"
    raw_text: str = Field(description="The exact text snippet mentioning date or time")
    normalized_datetime: Optional[str] = Field(None, description="ISO-8601 formatted datetime string YYYY-MM-DDTHH:MM:SS")
    description: str = Field(description="What is due or happening at this date/time")

class RecommendedAction(BaseModel):
    action_type: Literal["create_task_and_reminder", "archive_label", "escalate", "none"] = "none"
    requires_human_approval: bool = Field(default=False, description="True for sending emails, replies, or sensitive actions")
    draft_reply: Optional[str] = Field(None, description="Pre-composed contextual draft reply if a response is needed")

class GeminiAnalysisResult(BaseModel):
    is_spam: bool = Field(description="True if unsolicited spam, phishing, or scam")
    category: Literal["work", "personal", "promotional", "notification", "spam"]
    importance: Literal["high", "medium", "low"]
    is_actionable: bool = Field(description="True if recipient action or reply is required")
    priority: Literal["High", "Medium", "Low"]
    tasks: List[ExtractedTask] = Field(default_factory=list)
    events_deadlines: List[ExtractedDeadline] = Field(default_factory=list)
    recommended_action: RecommendedAction

def analyze_with_gemini(sender: str, sender_name: str, subject: str, body: str, timestamp_str: str = None) -> dict:
    """
    Analyzes an email using Google Gemini 2.5 Flash with Pydantic structured output.
    If GEMINI_API_KEY is not set or network fails, gracefully falls back to local models.
    """
    api_key = settings.GEMINI_API_KEY
    if not timestamp_str:
        timestamp_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    # If API key is provided, use live Gemini 2.5 Flash
    if api_key and api_key.startswith("AIza"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import ChatPromptTemplate

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.1,
                google_api_key=api_key
            )
            structured_llm = llm.with_structured_output(GeminiAnalysisResult)

            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an Autonomous AI Email & Task Management Assistant.
Thoroughly analyze the incoming email and extract structured task items, deadlines, priority, and draft replies.

REFERENCE TIME ANCHOR:
The email arrived at: {anchor_time} (Use this reference date to resolve relative dates like 'tomorrow at 5pm' or 'next Wednesday' into ISO-8601 YYYY-MM-DDTHH:MM:SS format).

RULES:
1. SPAM: Mark scams, fake prizes, and phishing as is_spam=True, category='spam', priority='Low'.
2. TASKS: Extract clear, actionable items in imperative form (e.g. 'Review slide deck', 'Submit invoice').
3. DEADLINES: Calculate exact future dates from the anchor time.
4. PRIORITY: High (urgent <48h, P0, critical review), Medium (standard 3-7 days), Low (routine, notifications).
5. HUMAN APPROVAL: Any outbound reply draft MUST have requires_human_approval=True.
"""),
                ("human", """SENDER: {sender_name} <{sender}>
SUBJECT: {subject}
DATE: {anchor_time}

BODY:
{body}
""")
            ])

            chain = prompt | structured_llm
            result: GeminiAnalysisResult = chain.invoke({
                "sender": sender,
                "sender_name": sender_name or "Sender",
                "subject": subject,
                "body": body,
                "anchor_time": timestamp_str
            })

            return result.model_dump()
        except Exception as e:
            print(f"[WARN] Live Gemini API call failed ({e}), using local trained model engine.")

    # Fallback to local high-accuracy engine
    from app.services.ai_inference_service import analyze_single_email
    return analyze_single_email(sender, sender_name, subject, body, timestamp_str)
