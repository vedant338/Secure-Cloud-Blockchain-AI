from cloud_storage.download_from_s3 import download_and_verify_file
from ai_ml.ai_service import analyze_file_risk


def verify_file_integrity(
    filename,
    aes_key,
    nonce,
    expected_hash,
    signature,
    public_key
):

    # 1️⃣ Call your cloud storage verification
    result = download_and_verify_file(
        filename=filename,
        aes_key=aes_key,
        nonce=nonce,
        expected_hash=expected_hash,
        signature_hex=signature,
        public_key_pem=public_key
    )

    # 2️⃣ AI risk analysis
    ai_result = analyze_file_risk(
        file_size=1,   # we don't know actual size after verify
        entropy=4.5,
        hash_length=len(expected_hash),
        verified=1 if result["verified"] else 0
    )

    # 3️⃣ Final response
    if result["verified"]:
        status = "AUTHENTIC"
        message = "File is safe and untampered"
    else:
        status = "TAMPERED"
        message = "WARNING: File integrity compromised"

    return {
        "status": status,
        "hash_valid": result["hash_valid"],
        "signature_valid": result["signature_valid"],
        "ai_risk": ai_result,
        "message": message
    }