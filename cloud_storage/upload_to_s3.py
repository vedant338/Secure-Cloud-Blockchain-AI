import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT_DIR))
                
import os
import io
import boto3
from dotenv import load_dotenv
from security.aes_crypto import encrypt_file
from security.hash_utils import sha256_hash
load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket = os.getenv("AWS_BUCKET_NAME")

# Sample data
data = b"This is a highly confidential file"

# Encrypt
encrypted_data, key, nonce = encrypt_file(data)
file_hash = sha256_hash(data)

# Upload encrypted file
s3.upload_fileobj(
    io.BytesIO(encrypted_data),
    bucket,
    "encrypted_file.bin"
)

print("Encrypted file uploaded to S3 successfully")
print("SHA-256 Hash of encrypted file:", file_hash)
print("AES Key (store securely):", key)
print("Nonce:", nonce)
