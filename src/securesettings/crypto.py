"""
توابع رمزنگاری و رمزگشایی
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def _get_key(password: str, salt: bytes = b'secure_settings_salt') -> bytes:
    """تولید کلید رمزنگاری از رمز عبور"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data: str, password: str) -> str:
    """
    رمزنگاری داده
    
    Args:
        data: داده متنی برای رمزنگاری
        password: رمز عبور
    
    Returns:
        داده رمزنگاری شده به صورت Base64
    """
    key = _get_key(password)
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data: str, password: str) -> str:
    """
    رمزگشایی داده
    
    Args:
        encrypted_data: داده رمزنگاری شده
        password: رمز عبور
    
    Returns:
        داده اصلی
    """
    key = _get_key(password)
    f = Fernet(key)
    decrypted = f.decrypt(base64.b64decode(encrypted_data))
    return decrypted.decode()
