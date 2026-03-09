import io
import boto3
from backend.config import Config
from security.aes_crypto import encrypt_file   # ✅ CORRECT
from security.hash_utils import sha256_hash
from security.ecdsa_utils import generate_ecdsa_keypair, sign_hash
from cryptography.hazmat.primitives import serialization

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

def process_and_upload_file(file_bytes: bytes, filename: str):
    # 🔐 ENCRYPT (NOT DECRYPT)
    encrypted_data, aes_key, nonce = encrypt_file(file_bytes)

    # 🔎 Hash original file
    file_hash = sha256_hash(file_bytes)

    # ✍️ Sign hash
    private_key, public_key = generate_ecdsa_keypair()
    signature = sign_hash(private_key, file_hash)

    encrypted_filename = f"{file_hash}.enc"

    # ☁️ Upload encrypted file
    s3.upload_fileobj(
        io.BytesIO(encrypted_data),
        Config.AWS_BUCKET_NAME,
        encrypted_filename
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    return {
        "encrypted_filename": encrypted_filename,
        "hash": file_hash,
        "signature": signature.hex(),
        "public_key": public_key_pem,
        "aes_key": aes_key.hex(),
        "nonce": nonce.hex()
    }