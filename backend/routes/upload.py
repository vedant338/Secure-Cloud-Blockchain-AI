from fastapi import APIRouter, UploadFile, File, Depends
from backend.services.upload_service import handle_upload
from backend.auth.deps import require_auth
import logging

router = APIRouter(prefix="/upload", tags=["Upload"])
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), username: str = Depends(require_auth)):
    logger.info("Upload started")

    content = await file.read()
    file_size = len(content)   # ✅ DEFINE IT HERE

    logger.info(f"File size: {file_size}")

    result = handle_upload(
        file_bytes=content,
        filename=file.filename
    )

    return {
        "message": "File uploaded securely",
        "filename": result["encrypted_filename"],
        "hash": result["hash"],
        "signature": result["signature"],
        "public_key": result["public_key"],
        "aes_key": result["aes_key"],
        "nonce": result["nonce"],
        "ai_analysis": result["ai_analysis"]
    }