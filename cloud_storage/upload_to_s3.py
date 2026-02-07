import os
import io
import sys
import boto3
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.insert(0,PROJECT_ROOT)
from security.aes_crypto import encrypt_file
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

# Upload encrypted file
s3.upload_fileobj(
    io.BytesIO(encrypted_data),
    bucket,
    "encrypted_file.bin"
)

print("Encrypted file uploaded to S3 successfully")
print("AES Key (store securely):", key)
print("Nonce:", nonce)
