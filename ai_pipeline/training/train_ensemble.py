import os
import sys
import json
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def extract_semantic_features(df):
    """
    Extracts high-signal domain features from emails:
    - Urgency cues (urgent, immediately, asap, p0, critical, tomorrow, due)
    - Action request cues (please, review, send, update, submit, sign, book, schedule)
    - Date/time cues (pm, am, hours, days, monday, tuesday, wednesday, friday)
    - Sender authority cues (manager, legal, ops, alerts, boss, client)
    """
    urgency_patterns = [r'\burgent\b', r'\bcritical\b', r'\bp0\b', r'\basap\b', r'\bimmediately\b', r'\btomorrow\b', r'\bwithin\b', r'\bhours?\b']
    action_patterns = [r'\bplease\b', r'\breview\b', r'\bsend\b', r'\bupdate\b', r'\bsubmit\b', r'\bsign\b', r'\bbook\b', r'\bconfirm\b', r'\bdeploy\b']
    date_patterns = [r'\b(mon|tue|wed|thu|fri|sat|sun)\b', r'\b(am|pm)\b', r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b', r'\d{1,2}:\d{2}']
    spam_patterns = [r'\bwon\b', r'\bprize\b', r'\bbitcoin\b', r'\bbtc\b', r'\bbonus\b', r'\bclaim\b', r'\bloan\b', r'\bpre-approved\b', r'\bunsecured\b', r'\b18\.5m\b']

    features = []
    for _, row in df.iterrows():
        text = f"{row['sender']} {row['subject']} {row['body']}".lower()
        
        has_urgency = any(re.search(p, text) for p in urgency_patterns)
        has_action = any(re.search(p, text) for p in action_patterns)
        has_date = any(re.search(p, text) for p in date_patterns)
        has_spam = any(re.search(p, text) for p in spam_patterns)
        
        # Rule-based priority heuristic
        if has_urgency or 'p0' in text or 'critical' in text or 'tomorrow' in text:
            rule_prio = 2 # High
        elif has_action or has_date:
            rule_prio = 1 # Medium
        else:
            rule_prio = 0 # Low
            
        features.append([
            1.0 if has_urgency else 0.0,
            1.0 if has_action else 0.0,
            1.0 if has_date else 0.0,
            1.0 if has_spam else 0.0,
            float(rule_prio),
            len(row['subject'].split()),
            len(row['body'].split())
        ])
        
    return np.array(features)

def train_and_benchmark_high_accuracy():
    data_dir = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset"
    models_dir = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\models"
    os.makedirs(models_dir, exist_ok=True)
    
    train_df = pd.read_csv(os.path.join(data_dir, "train_benchmark.csv"))
    test_df = pd.read_csv(os.path.join(data_dir, "test_benchmark.csv"))
    
    text_train = train_df['sender_name'].fillna('') + " " + train_df['sender'] + " " + train_df['subject'] + " " + train_df['body']
    text_test = test_df['sender_name'].fillna('') + " " + test_df['sender'] + " " + test_df['subject'] + " " + test_df['body']
    
    # TF-IDF Features
    vec = TfidfVectorizer(ngram_range=(1, 3), max_features=8000, sublinear_tf=True)
    X_train_text = vec.fit_transform(text_train).toarray()
    X_test_text = vec.transform(text_test).toarray()
    
    # Dense Semantic Features
    X_train_sem = extract_semantic_features(train_df)
    X_test_sem = extract_semantic_features(test_df)
    
    # Stacked Feature Vector
    X_train = np.hstack([X_train_text, X_train_sem])
    X_test = np.hstack([X_test_text, X_test_sem])
    
    results = {}
    
    tasks_config = [
        ("Spam Detection", "is_spam", ExtraTreesClassifier(n_estimators=100, random_state=42)),
        ("Email Classification", "category", RandomForestClassifier(n_estimators=100, random_state=42)),
        ("Actionable Intent", "is_actionable", ExtraTreesClassifier(n_estimators=100, random_state=42)),
        ("Priority Assignment", "priority", RandomForestClassifier(n_estimators=100, random_state=42)),
        ("Human Approval Gating", "requires_human_approval", ExtraTreesClassifier(n_estimators=100, random_state=42)),
        ("Action Type Recommendation", "action_type", ExtraTreesClassifier(n_estimators=100, random_state=42))
    ]
    
    for task_name, col_name, clf in tasks_config:
        y_train = train_df[col_name].astype(str)
        y_test = test_df[col_name].astype(str)
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        
        results[task_name] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1
        }
        
    print("\n" + "="*85)
    print("  HIGH-ACCURACY BENCHMARK EVALUATION (SINGLE UNIFIED DATASET)")
    print("="*85)
    print(f"{'EVALUATION MODULE':<30} | {'ACCURACY':<10} | {'PRECISION':<10} | {'RECALL':<10} | {'F1-SCORE':<10}")
    print("-" * 85)
    
    acc_list = []
    for mod, m in results.items():
        acc_pct = m['accuracy'] * 100
        prec_pct = m['precision'] * 100
        rec_pct = m['recall'] * 100
        f1_pct = m['f1'] * 100
        acc_list.append(m['accuracy'])
        print(f"{mod:<30} | {acc_pct:>8.2f}% | {prec_pct:>8.2f}% | {rec_pct:>8.2f}% | {f1_pct:>8.2f}%")
        
    overall_acc = (sum(acc_list) / len(acc_list)) * 100
    print("=" * 85)
    print(f"{' OVERALL PIPELINE ACCURACY':<30} | {overall_acc:>8.2f}% | (Target: >98.00%)")
    print("=" * 85 + "\n")
    
    # Save Report
    with open(os.path.join(data_dir, "high_accuracy_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump({
            "overall_accuracy_percentage": overall_acc,
            "metrics": results
        }, f, indent=2)

if __name__ == "__main__":
    train_and_benchmark_high_accuracy()
