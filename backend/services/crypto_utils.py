from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


def generate_key():
    """Generate a new Fernet encryption key"""
    return Fernet.generate_key()


def encrypt_data(data: str, key: bytes) -> str:
    """Encrypt a string using Fernet symmetric encryption"""
    f = Fernet(key)
    encrypted = f.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """Decrypt a Fernet-encrypted string"""
    f = Fernet(key)
    decrypted = f.decrypt(base64.b64decode(encrypted_data))
    return decrypted.decode('utf-8')


def derive_key_from_password(password: str, salt: bytes = None) -> tuple:
    """Derive an encryption key from a password using PBKDF2"""
    if salt is None:
        salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt
