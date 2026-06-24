"""
کلاس اصلی برای مدیریت تنظیمات امن
"""

import os
import json
import base64
import shutil
from pathlib import Path
from typing import Any, Optional, Dict
from .crypto import encrypt_data, decrypt_data

class Settings:
    """
    کلاس مدیریت تنظیمات امن
    
    Examples:
        >>> settings = Settings("my_app", password="1234")
        >>> settings.set("api_key", "secret123")
        >>> settings.set("debug", True)
        >>> settings.save()
    """
    
    def __init__(self, name: str, password: str = None, encrypt: bool = True):
        """
        مقداردهی اولیه تنظیمات
        
        Args:
            name: نام تنظیمات (برای نام فایل استفاده می‌شود)
            password: رمز عبور برای رمزنگاری (اگر None باشد، از متغیر محیطی گرفته می‌شود)
            encrypt: آیا تنظیمات رمزنگاری شوند؟
        """
        self.name = name
        self.encrypt = encrypt
        self._data: Dict[str, Any] = {}
        
        # تعیین رمز عبور
        if password is None:
            self.password = os.environ.get("SECURE_SETTINGS_PASSWORD", "")
        else:
            self.password = password
        
        # مسیر فایل تنظیمات
        self.file_path = Path.home() / f".{name}_settings.enc"
        
        # بارگذاری تنظیمات قبلی اگر وجود داشت
        if self.file_path.exists():
            self._load()
    
    def _load(self):
        """بارگذاری تنظیمات از فایل"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if self.encrypt and self.password:
                content = decrypt_data(content, self.password)
            
            self._data = json.loads(content)
        except Exception as e:
            raise ValueError(f"خطا در بارگذاری تنظیمات: رمز عبور اشتباه است یا فایل خراب شده است") from e
    
    def save(self):
        """ذخیره تنظیمات در فایل"""
        content = json.dumps(self._data, ensure_ascii=False, indent=2)
        
        if self.encrypt and self.password:
            content = encrypt_data(content, self.password)
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def set(self, key: str, value: Any):
        """
        تنظیم یک مقدار
        
        Args:
            key: کلید تنظیمات
            value: مقدار مورد نظر
        """
        self._data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        دریافت یک مقدار
        
        Args:
            key: کلید تنظیمات
            default: مقدار پیش‌فرض در صورت نبودن کلید
        """
        return self._data.get(key, default)
    
    def delete(self, key: str):
        """حذف یک کلید از تنظیمات"""
        if key in self._data:
            del self._data[key]
    
    def clear(self):
        """پاک کردن همه تنظیمات"""
        self._data = {}
    
    def get_all(self) -> Dict[str, Any]:
        """دریافت همه تنظیمات"""
        return self._data.copy()
    
    def has(self, key: str) -> bool:
        """بررسی وجود یک کلید"""
        return key in self._data
    
    def backup(self):
        """ایجاد پشتیبان از تنظیمات فعلی"""
        backup_path = self.file_path.with_suffix(".enc.backup")
        if self.file_path.exists():
            shutil.copy2(self.file_path, backup_path)
    
    def restore_backup(self):
        """بازگردانی از پشتیبان"""
        backup_path = self.file_path.with_suffix(".enc.backup")
        if backup_path.exists():
            shutil.copy2(backup_path, self.file_path)
            self._load()
    
    def reset(self):
        """بازنشانی تنظیمات به حالت اولیه"""
        if self.file_path.exists():
            os.remove(self.file_path)
        self._data = {}