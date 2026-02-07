from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

# Generate ECDSA key pair
def generate_ecdsa_keypair():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    return private_key, public_key


# Sign SHA-256 hash using ECDSA
def sign_hash(private_key, file_hash: str) -> bytes:
    signature = private_key.sign(
        bytes.fromhex(file_hash),
        ec.ECDSA(hashes.SHA256())
    )
    return signature


# Verify ECDSA signature
def verify_signature(public_key, file_hash: str, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            bytes.fromhex(file_hash),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False