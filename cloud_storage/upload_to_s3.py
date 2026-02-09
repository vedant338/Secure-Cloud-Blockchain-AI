import io
import boto3
from backend.config import Config
from security.aes_crypto import encrypt_file
from security.hash_utils import sha256_hash
from security.ecdsa_utils import (
    generate_ecdsa_keypair,
    sign_hash,
    verify_signature
)

# Create S3 client ONCE
s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

def process_and_upload_file(file_bytes: bytes, filename: str):
    """
    Encrypts file, hashes it, signs hash, uploads encrypted file to S3
    """

    # Encrypt
    encrypted_data, key, nonce = encrypt_file(file_bytes)

    # Hash original data
    file_hash = sha256_hash(file_bytes)

    # Sign hash
    private_key, public_key = generate_ecdsa_keypair()
    signature = sign_hash(private_key, file_hash)

    # Upload encrypted file
    s3.upload_fileobj(
        io.BytesIO(encrypted_data),
        Config.AWS_BUCKET_NAME,
        filename
    )

    return {
        "filename": filename,
        "hash": file_hash,
        "signature": signature.hex(),
        "public_key": public_key.hex(),
        "aes_key": key.hex(),
        "nonce": nonce.hex()
    }