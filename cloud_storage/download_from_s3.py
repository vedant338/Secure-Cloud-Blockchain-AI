import io
import boto3
from backend.config import Config
from security.aes_crypto import decrypt_file
from security.hash_utils import sha256_hash
from security.ecdsa_utils import verify_signature
from cryptography.hazmat.primitives.serialization import load_pem_public_key

s3 = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)

def download_and_verify_file(
    filename: str,
    aes_key: str,
    nonce: str,
    expected_hash: str,
    signature_hex: str,
    public_key_pem: str
):
    # 1️⃣ Download encrypted file
    buffer = io.BytesIO()
    s3.download_fileobj(Config.AWS_BUCKET_NAME, filename, buffer)
    encrypted_data = buffer.getvalue()

    # 2️⃣ Decrypt
    decrypted_data = decrypt_file(
        encrypted_data,
        bytes.fromhex(aes_key),
        bytes.fromhex(nonce)
    )

    # 3️⃣ Hash
    computed_hash = sha256_hash(decrypted_data)

    # 4️⃣ Verify hash
    hash_valid = computed_hash == expected_hash

    # 5️⃣ Verify signature
    clean_public_key = public_key_pem.replace("\\n","\n")
    public_key = load_pem_public_key(clean_public_key.encode())
    signature_valid = verify_signature(
        public_key,
        computed_hash,
        bytes.fromhex(signature_hex)
    )

    return {
        "hash_valid": hash_valid,
        "signature_valid": signature_valid,
        "verified": hash_valid and signature_valid
    }


def download_decrypted_file(
    filename: str,
    aes_key: str,
    nonce: str,
    expected_hash: str,
    signature_hex: str,
    public_key_pem: str
) -> bytes:
    buffer = io.BytesIO()
    s3.download_fileobj(Config.AWS_BUCKET_NAME, filename, buffer)
    encrypted_data = buffer.getvalue()

    decrypted_data = decrypt_file(
        encrypted_data,
        bytes.fromhex(aes_key),
        bytes.fromhex(nonce)
    )
    computed_hash = sha256_hash(decrypted_data)
    if computed_hash != expected_hash:
        raise ValueError("Hash mismatch - file integrity failed")

    clean_public_key = public_key_pem.replace("\\n", "\n")
    public_key = load_pem_public_key(clean_public_key.encode())
    if not verify_signature(public_key, computed_hash, bytes.fromhex(signature_hex)):
        raise ValueError("Signature verification failed")

    return decrypted_data