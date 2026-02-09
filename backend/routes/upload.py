from fastapi import APIRouter, UploadFile, File
from cloud_storage.upload_to_s3 import process_and_upload_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    result = process_and_upload_file(
        file_bytes=content,
        filename=file.filename
    )

    return {
        "message": "File uploaded securely",
        "metadata": result
    }