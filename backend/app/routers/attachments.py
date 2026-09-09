import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Attachment, Email, AuditLog
from app.schemas.attachment_schemas import AttachmentResponse, AttachmentUploadResponse
from app.services.cloudinary_service import upload_file_bytes, delete_cloudinary_file, is_cloudinary_configured

router = APIRouter(prefix="/api/attachments", tags=["Cloudinary Attachments & Media"])

@router.get("/status")
def get_cloudinary_status():
    """Checks if live Cloudinary credentials are configured."""
    configured = is_cloudinary_configured()
    return {
        "provider": "Cloudinary",
        "live_credentials_configured": configured,
        "mode": "LIVE_CLOUD_CDN" if configured else "LOCAL_SIMULATOR_FALLBACK",
        "status": "ready"
    }

@router.post("/upload", response_model=AttachmentUploadResponse)
async def upload_attachment(
    file: UploadFile = File(..., description="File to upload to Cloudinary (PDF, PNG, JPG, DOCX)"),
    email_id: Optional[int] = Form(None, description="Optional email ID to attach to"),
    db: Session = Depends(get_db)
):
    """
    Uploads an email attachment to Cloudinary CDN and saves metadata in database.
    """
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    upload_res = upload_file_bytes(
        file_bytes=file_bytes,
        filename=file.filename or "attachment.bin",
        folder="ai_email_assistant/attachments"
    )

    attachment_obj = Attachment(
        email_id=email_id,
        task_id=None,
        filename=file.filename or "attachment.bin",
        file_type=upload_res["file_type"],
        file_size_bytes=upload_res["file_size_bytes"],
        cloudinary_url=upload_res["cloudinary_url"],
        cloudinary_public_id=upload_res["cloudinary_public_id"]
    )
    db.add(attachment_obj)

    audit = AuditLog(
        entity_type="ATTACHMENT",
        entity_id=str(file.filename),
        action="UPLOADED_TO_CLOUDINARY",
        performed_by="USER",
        details=f"Uploaded {file.filename} ({upload_res['file_size_bytes']} bytes) to Cloudinary: {upload_res['cloudinary_url']}"
    )
    db.add(audit)
    db.commit()
    db.refresh(attachment_obj)

    return AttachmentUploadResponse(
        success=True,
        message=f"File '{file.filename}' successfully uploaded to Cloudinary CDN!",
        attachment=AttachmentResponse.model_validate(attachment_obj)
    )

@router.get("", response_model=List[AttachmentResponse])
def get_attachments(
    email_id: Optional[int] = Query(None, description="Filter attachments by email ID (e.g. 9) or leave blank for ALL"),
    db: Session = Depends(get_db)
):
    """Retrieve attachments stored in Cloudinary (filter by email_id or leave blank for all)."""
    query = db.query(Attachment)
    if email_id is not None:
        query = query.filter(Attachment.email_id == email_id)
    return query.order_by(Attachment.uploaded_at.desc(), Attachment.id.desc()).all()
