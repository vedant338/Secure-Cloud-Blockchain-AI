from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import Response
from cloud_storage.download_from_s3 import download_and_verify_file, download_decrypted_file
from backend.auth.deps import require_auth

router = APIRouter(prefix="/download", tags=["Download"])

@router.post("/file")
async def download_file(
    username: str = Depends(require_auth),
    filename: str = Query(...),
    aes_key: str = Query(...),
    nonce: str = Query(...),
    expected_hash: str = Query(..., alias="expected_hash"),
    signature_hex: str = Query(...),
    public_key_pem: str = Query(...),
    original_filename: str | None = Query(None),
):
    try:
        data = download_decrypted_file(
            filename=filename,
            aes_key=aes_key,
            nonce=nonce,
            expected_hash=expected_hash,
            signature_hex=signature_hex,
            public_key_pem=public_key_pem,
        )
        disp = f'attachment; filename="{original_filename or filename}"'
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": disp},
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify")
async def verify_download(
    filename: str, 
    aes_key: str,
    nonce: str,
    expected_hash: str,
    signature_hex: str,
    public_key_pem: str
):
    return download_and_verify_file(
        filename=filename,
        aes_key=aes_key,
        nonce=nonce,
        expected_hash=expected_hash,
        signature_hex=signature_hex,
        public_key_pem=public_key_pem
    )