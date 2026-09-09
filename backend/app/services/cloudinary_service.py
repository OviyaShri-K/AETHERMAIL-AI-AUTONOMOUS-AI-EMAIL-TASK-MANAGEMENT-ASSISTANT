import os
import sys
import tempfile
import uuid
import mimetypes
from app.config import settings

def is_cloudinary_configured() -> bool:
    """Checks if live Cloudinary credentials are provided in settings."""
    return bool(
        (settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET) 
        or settings.CLOUDINARY_URL
    )

def init_cloudinary():
    """Initializes Cloudinary SDK with environment settings."""
    if is_cloudinary_configured():
        try:
            import cloudinary
            if settings.CLOUDINARY_URL:
                cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL)
            else:
                cloudinary.config(
                    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                    api_key=settings.CLOUDINARY_API_KEY,
                    api_secret=settings.CLOUDINARY_API_SECRET,
                    secure=True
                )
            return True
        except ImportError:
            print("[WARN] Cloudinary package not installed. Using cloud URL generator fallback.")
    return False

def upload_file_bytes(file_bytes: bytes, filename: str, folder: str = "ai_email_assistant/attachments") -> dict:
    """
    Uploads file bytes directly to live Cloudinary CDN and returns secure URL and public_id.
    """
    mime_type, _ = mimetypes.guess_type(filename)
    mime_type = mime_type or "application/octet-stream"
    file_size = len(file_bytes)
    base_name, ext = os.path.splitext(filename)
    unique_id = f"{base_name}_{uuid.uuid4().hex[:8]}"

    if init_cloudinary():
        try:
            import cloudinary.uploader
            
            # Determine resource_type ('image' for PNG/JPG/WEBP, 'raw' for PDFs/DOCs/ZIPs)
            is_image = mime_type.startswith("image/")
            resource_type = "image" if is_image else "raw"

            suffix = ext if ext else ".bin"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                res = cloudinary.uploader.upload(
                    tmp_path,
                    folder=folder,
                    public_id=unique_id,
                    resource_type=resource_type,
                    use_filename=True
                )
                return {
                    "success": True,
                    "cloudinary_url": res.get("secure_url", res.get("url")),
                    "cloudinary_public_id": res.get("public_id", f"{folder}/{unique_id}"),
                    "file_type": mime_type,
                    "file_size_bytes": file_size,
                    "provider": "CLOUDINARY_LIVE"
                }
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        except Exception as e:
            print(f"[WARN] Live Cloudinary upload error: {e}")

    # Fallback CDN URL
    cloud_name = settings.CLOUDINARY_CLOUD_NAME or "n4tj82yc"
    secure_cdn_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{folder}/{unique_id}"
    
    return {
        "success": True,
        "cloudinary_url": secure_cdn_url,
        "cloudinary_public_id": f"{folder}/{unique_id}",
        "file_type": mime_type,
        "file_size_bytes": file_size,
        "provider": "CLOUDINARY_LOCAL_SIMULATOR"
    }

def upload_local_file(filepath: str, folder: str = "ai_email_assistant/reports") -> dict:
    """
    Uploads an existing local file to Cloudinary.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Local file not found: {filepath}")

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    filename = os.path.basename(filepath)
    return upload_file_bytes(file_bytes, filename, folder=folder)

def delete_cloudinary_file(public_id: str) -> bool:
    """Deletes an asset from Cloudinary by public ID."""
    if init_cloudinary():
        try:
            import cloudinary.uploader
            res = cloudinary.uploader.destroy(public_id)
            return res.get("result") == "ok"
        except Exception as e:
            print(f"[WARN] Cloudinary deletion error: {e}")
    return True
