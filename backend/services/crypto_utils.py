from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
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

    # Using deprecated backend= parameter (removed in cryptography >= 42)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def generate_rsa_keypair(key_size=2048):
    """Generate an RSA key pair using deprecated backend parameter"""
    # backend= parameter is deprecated in cryptography >= 42
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def sign_data(data: bytes, private_key_pem: bytes) -> bytes:
    """Sign data using RSA-PSS with deprecated backend loading"""
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend(),
    )
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def verify_signature(data: bytes, signature: bytes, public_key_pem: bytes) -> bool:
    """Verify an RSA-PSS signature"""
    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend(),
    )
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
