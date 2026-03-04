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
        return os.getenv('PHONE', '')  # اختياري الآن - قد لا تحتاجه
    
    # ✅ إضافة خاصية البوت توكن الجديدة
    @property
    def BOT_TOKEN(self):
        return os.getenv('BOT_TOKEN', '')
    
    # إعدادات الجروب المستهدف - تم تغييرها إلى رابط دعوة
    @property
    def TARGET_GROUP_INVITE(self):
        return os.getenv('TARGET_GROUP_INVITE', '')
    
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
    # ✅ إضافة متغير الكلاس للبوت توكن
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    TARGET_GROUP_INVITE = os.getenv('TARGET_GROUP_INVITE', '')

    @classmethod
    def validate(cls):
        """التحقق من صحة الإعدادات"""
        # إعادة تحميل المتغيرات للتأكد من قراءتها من البيئة الحالية
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        # ✅ PHONE أصبح اختيارياً الآن
        phone = os.getenv('PHONE', '')
        # ✅ إضافة التحقق من البوت توكن
        bot_token = os.getenv('BOT_TOKEN')
        target_group_invite = os.getenv('TARGET_GROUP_INVITE')
        
        errors = []
        
        if not api_id or api_id == '0':
            errors.append("API_ID مطلوب في ملف .env")
        if not api_hash:
            errors.append("API_HASH مطلوب في ملف .env")
        # ✅ التحقق من وجود البوت توكن (مطلوب الآن)
        if not bot_token:
            errors.append("BOT_TOKEN مطلوب في ملف .env (يمكنك الحصول عليه من @BotFather)")
        # ✅ PHONE أصبح اختيارياً - يمكن إزالته لاحقاً
        if not target_group_invite:
            errors.append("رابط الدعوة (TARGET_GROUP_INVITE) مطلوب في ملف .env")
            
        if errors:
            raise ValueError(f"❌ أخطاء في التكوين:\n" + "\n".join(f"  • {error}" for error in errors))
            
        # تحديث قيم الكلاس بعد التحقق
        cls.API_ID = int(api_id)
        cls.API_HASH = api_hash
        cls.PHONE = phone
        # ✅ إضافة البوت توكن
        cls.BOT_TOKEN = bot_token
        cls.TARGET_GROUP_INVITE = target_group_invite
        
        return True
        
    @classmethod
    def print_config(cls):
        """عرض الإعدادات الحالية"""
        print("\n" + "="*50)
        print("⚙️  إعدادات البوت")
        print("="*50)
        # ✅ تعديل العرض - إظهار البوت توكن بدلاً من رقم الهاتف
        print(f"🤖 حالة البوت: {'تم إعداد البوت توكن' if cls.BOT_TOKEN else '⚠️ البوت توكن غير مضبوط'}")
        print(f"🔗 رابط الجروب المستهدف: {cls.TARGET_GROUP_INVITE}")
        print(f"⏱️  التأخير: {cls.MIN_DELAY} - {cls.MAX_DELAY} ثانية")
        print(f"📊 طول الرسالة: {cls.MIN_MESSAGE_LENGTH} - {cls.MAX_MESSAGE_LENGTH}")
        print(f"🔒 الحماية من الحظر: مفعلة")
        print(f"📝 التسجيل: {'مفعّل' if cls.ENABLE_LOGGING else 'معطل'}")
        print("="*50 + "\n")
