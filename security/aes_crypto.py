from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_file(data: bytes):
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    return encrypted_data, key, nonce

def decrypt_file(encrypted_data, key, nonce):
    aesgcm = AESGCM(key)
    decrypt_data = aesgcm.decrypt(nonce, encrypted_data, None)
    return decrypt_data