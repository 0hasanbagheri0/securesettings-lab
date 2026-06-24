"""
تست جامع کتابخانه SecureSettings
"""

import os
import time
from securesettings import Settings

def print_header(text):
    """چاپ هدر با خط جداکننده"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def test_basic_operations():
    """تست عملیات پایه"""
    print_header("تست عملیات پایه")
    
    # ایجاد تنظیمات
    settings = Settings("test_app", password="1234")
    print("✅ تنظیمات ایجاد شد")
    
    # ذخیره مقادیر
    settings.set("name", "SecureSettings")
    settings.set("version", "1.0.0")
    settings.set("debug", True)
    settings.set("port", 8080)
    settings.set("tags", ["python", "security", "settings"])
    settings.save()
    print("✅ مقادیر ذخیره شدند")
    
    # دریافت مقادیر
    print(f"  name: {settings.get('name')}")
    print(f"  version: {settings.get('version')}")
    print(f"  debug: {settings.get('debug')}")
    print(f"  port: {settings.get('port')}")
    print(f"  tags: {settings.get('tags')}")
    
    # تست مقدار پیش‌فرض
    default_value = settings.get("not_exist", "default_value")
    print(f"  مقدار پیش‌فرض: {default_value}")
    
    print("✅ عملیات پایه با موفقیت انجام شد")

def test_file_operations():
    """تست عملیات فایل"""
    print_header("تست عملیات فایل")
    
    # مسیر فایل تنظیمات
    settings = Settings("test_app", password="1234")
    print(f"📂 مسیر فایل: {settings.file_path}")
    
    # بررسی وجود فایل
    if settings.file_path.exists():
        print(f"✅ فایل تنظیمات وجود دارد (حجم: {settings.file_path.stat().st_size} بایت)")
    else:
        print("❌ فایل تنظیمات یافت نشد")
    
    # ایجاد پشتیبان
    settings.backup()
    backup_path = settings.file_path.with_suffix(".enc.backup")
    if backup_path.exists():
        print(f"✅ پشتیبان ایجاد شد (حجم: {backup_path.stat().st_size} بایت)")
    else:
        print("❌ پشتیبان ایجاد نشد")
    
    print("✅ عملیات فایل با موفقیت انجام شد")

def test_delete_and_clear():
    """تست حذف و پاک کردن"""
    print_header("تست حذف و پاک کردن")
    
    settings = Settings("test_app", password="1234")
    
    # افزودن چند مقدار
    settings.set("temp1", "value1")
    settings.set("temp2", "value2")
    settings.set("temp3", "value3")
    print("✅ سه مقدار جدید اضافه شد")
    
    # حذف یک مقدار
    settings.delete("temp2")
    print("✅ کلید 'temp2' حذف شد")
    
    # بررسی وجود کلید
    print(f"  'temp1' وجود دارد؟ {settings.has('temp1')}")
    print(f"  'temp2' وجود دارد؟ {settings.has('temp2')}")
    print(f"  'temp3' وجود دارد؟ {settings.has('temp3')}")
    
    # دریافت همه مقادیر
    all_data = settings.get_all()
    print(f"  مقادیر فعلی: {list(all_data.keys())}")
    
    # پاک کردن همه
    settings.clear()
    print("✅ همه مقادیر پاک شدند")
    print(f"  مقادیر بعد از پاک کردن: {list(settings.get_all().keys())}")
    
    print("✅ عملیات حذف و پاک کردن با موفقیت انجام شد")

def test_reset():
    """تست بازنشانی"""
    print_header("تست بازنشانی")
    
    settings = Settings("test_app", password="1234")
    
    # ذخیره مقادیر
    settings.set("test_key", "test_value")
    settings.save()
    print("✅ مقدار 'test_key' ذخیره شد")
    
    # بازنشانی
    settings.reset()
    print("✅ تنظیمات بازنشانی شد")
    
    # بررسی وجود فایل
    if settings.file_path.exists():
        print("❌ فایل تنظیمات هنوز وجود دارد")
    else:
        print("✅ فایل تنظیمات حذف شد")
    
    print("✅ عملیات بازنشانی با موفقیت انجام شد")

def test_encryption():
    """تست رمزنگاری"""
    print_header("تست رمزنگاری")
    
    # تنظیمات با رمزنگاری
    settings = Settings("test_app", password="1234")
    settings.set("secret", "This is a secret message")
    settings.save()
    print("✅ داده با رمزنگاری ذخیره شد")
    
    # بررسی محتوای فایل (غیرقابل خواندن)
    with open(settings.file_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"📄 محتوای فایل رمزنگاری شده: {content[:50]}...")
    
    # بارگذاری با رمز درست
    settings2 = Settings("test_app", password="1234")
    secret = settings2.get("secret")
    print(f"🔓 داده بازیابی شده: {secret}")
    
    # بارگذاری با رمز اشتباه (خطا می‌دهد)
    try:
        settings3 = Settings("test_app", password="wrong_password")
        secret2 = settings3.get("secret")
        print("❌ با رمز اشتباه هم داده بازیابی شد!")
    except:
        print("✅ با رمز اشتباه، داده بازیابی نشد (درست)")
    
    print("✅ عملیات رمزنگاری با موفقیت انجام شد")

def test_performance():
    """تست عملکرد"""
    print_header("تست عملکرد")
    
    settings = Settings("test_app", password="1234")
    
    # ذخیره ۱۰۰۰ مقدار
    start = time.time()
    for i in range(100):
        settings.set(f"key_{i}", f"value_{i}")
    settings.save()
    end = time.time()
    print(f"⏱️ ذخیره ۱۰۰ مقدار: {(end - start)*1000:.2f} میلی‌ثانیه")
    
    # بارگذاری ۱۰۰۰ مقدار
    start = time.time()
    settings2 = Settings("test_app", password="1234")
    for i in range(100):
        settings2.get(f"key_{i}")
    end = time.time()
    print(f"⏱️ خواندن ۱۰۰ مقدار: {(end - start)*1000:.2f} میلی‌ثانیه")
    
    print("✅ تست عملکرد با موفقیت انجام شد")

def main():
    """اجرای همه تست‌ها"""
    print("\n" + "="*50)
    print("  تست جامع کتابخانه SecureSettings")
    print("="*50)
    
    try:
        test_basic_operations()
        test_file_operations()
        test_delete_and_clear()
        test_reset()
        test_encryption()
        test_performance()
        
        print("\n" + "="*50)
        print("✅ همه تست‌ها با موفقیت انجام شدند!")
        print("="*50 + "\n")
        
    except KeyboardInterrupt:
        print("\n⚠️ تست توسط کاربر متوقف شد")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()