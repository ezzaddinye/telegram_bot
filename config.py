"""
ملف التكوين المتقدم للبوت
Advanced Bot Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """فئة التكوين الرئيسية"""
    
    # إعدادات API
    @property
    def API_ID(self):
        return int(os.getenv('API_ID', 0))

    @property
    def API_HASH(self):
        return os.getenv('API_HASH', '')

    @property
    def PHONE(self):
        return os.getenv('PHONE', '')
    
    # إعدادات الجروب المستهدف
    @property
    def TARGET_GROUP_ID(self):
        return int(os.getenv('TARGET_GROUP_ID', 0))
    
    # إعدادات التأخير (ثوانٍ)
    MIN_DELAY = float(os.getenv('MIN_DELAY', 0.5))
    MAX_DELAY = float(os.getenv('MAX_DELAY', 3.0))
    
    # إعدادات التسجيل
    ENABLE_LOGGING = os.getenv('ENABLE_LOGGING', 'true').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # إعدادات تحليل المحتوى
    MIN_MESSAGE_LENGTH = int(os.getenv('MIN_MESSAGE_LENGTH', 10))
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', 10000))
    
    # إعدادات الحماية من الحظر
    FLOOD_WAIT_MULTIPLIER = float(os.getenv('FLOOD_WAIT_MULTIPLIER', 1.5))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # إعدادات الجروبات المراقبة
    MONITORED_GROUPS = []
    
    # تحويل الخصائص إلى متغيرات كلاس لسهولة الوصول
    API_ID = int(os.getenv('API_ID', 0))
    API_HASH = os.getenv('API_HASH', '')
    PHONE = os.getenv('PHONE', '')
    TARGET_GROUP_ID = int(os.getenv('TARGET_GROUP_ID', 0))
    

    @classmethod
    def validate(cls):
        """التحقق من صحة الإعدادات"""
        # إعادة تحميل المتغيرات للتأكد من قراءتها من البيئة الحالية
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone = os.getenv('PHONE')
        target_group_id = os.getenv('TARGET_GROUP_ID')
        
        errors = []
        
        if not api_id or api_id == '0':
            errors.append("API_ID مطلوب في ملف .env")
        if not api_hash:
            errors.append("API_HASH مطلوب في ملف .env")
        if not phone:
            errors.append("رقم الهاتف (PHONE) مطلوب في ملف .env")
        if not target_group_id or target_group_id == '0':
            errors.append("TARGET_GROUP_ID مطلوب في ملف .env")
            
        if errors:
            raise ValueError(f"❌ أخطاء في التكوين:\n" + "\n".join(f"  • {error}" for error in errors))
            
        # تحديث قيم الكلاس بعد التحقق
        cls.API_ID = int(api_id)
        cls.API_HASH = api_hash
        cls.PHONE = phone
        cls.TARGET_GROUP_ID = int(target_group_id)
        
        return True
        
    @classmethod
    def print_config(cls):
        """عرض الإعدادات الحالية"""
        print("\n" + "="*50)
        print("⚙️  إعدادات البوت")
        print("="*50)
        print(f"📱 رقم الهاتف: {cls.PHONE}")
        print(f"🎯 معرف الجروب المستهدف: {cls.TARGET_GROUP_ID}")
        print(f"⏱️  التأخير: {cls.MIN_DELAY} - {cls.MAX_DELAY} ثانية")
        print(f"📊 طول الرسالة: {cls.MIN_MESSAGE_LENGTH} - {cls.MAX_MESSAGE_LENGTH}")
        print(f"🔒 الحماية من الحظر: مفعلة")
        print(f"📝 التسجيل: {'مفعّل' if cls.ENABLE_LOGGING else 'معطل'}")
        print("="*50 + "\n")
