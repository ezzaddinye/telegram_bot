import asyncio
import os
import sys
from multi_account_manager import MultiAccountManager
from admin_panel import AdminPanel
from config import Config
from database import Database

async def main():
    print("🌟 نظام إدارة حسابات تيليجرام المتطور يبدأ الآن...")
    
    # التأكد من وجود مجلد الجلسات
    if not os.path.exists('sessions'):
        os.makedirs('sessions')

    # تهيئة قاعدة البيانات
    db = Database()
    
    # تحميل الإعدادات
    ADMIN_BOT_TOKEN = os.getenv('ADMIN_BOT_TOKEN')
    ADMIN_ID = os.getenv('ADMIN_ID')

    tasks = []

    # 1. تشغيل مدير الحسابات المتعددة
    manager = MultiAccountManager()
    tasks.append(manager.run_all())

    # 2. تشغيل لوحة تحكم المدير (إذا كانت الإعدادات متوفرة)
    if ADMIN_BOT_TOKEN and ADMIN_ID:
        panel = AdminPanel(ADMIN_BOT_TOKEN, Config.API_ID, Config.API_HASH, ADMIN_ID)
        # بما أن AdminPanel.run تستخدم run_until_disconnected، سنقوم بتشغيلها كمهمة
        tasks.append(panel.client.run_until_disconnected())
        print("✅ تم تشغيل لوحة التحكم بنجاح")
    else:
        print("⚠️ تحذير: لم يتم تشغيل لوحة التحكم لعدم وجود ADMIN_BOT_TOKEN أو ADMIN_ID في .env")

    # تشغيل الكل
    if tasks:
        await asyncio.gather(*tasks)
    else:
        print("❌ لا توجد مهام للتشغيل. يرجى التحقق من الإعدادات.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف النظام.")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")
