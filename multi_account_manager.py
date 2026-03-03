import asyncio
import logging
from telethon import TelegramClient, events
from database import Database
from message_analyzer_v2 import MessageAnalyzerV2
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAccountManager:
    def __init__(self):
        self.db = Database()
        self.analyzer = MessageAnalyzerV2(db=self.db)
        self.clients = []
        self.ad_tasks = []

    async def start_worker(self, account_data):
        """تشغيل حساب مراقبة ونقل رسائل"""
        phone, api_id, api_hash, session_name = account_data[1], account_data[2], account_data[3], account_data[4]
        client = TelegramClient(f"sessions/{session_name}", api_id, api_hash)
        
        @client.on(events.NewMessage(incoming=True))
        async def handler(event):
            if event.is_private: return
            
            analysis = await self.analyzer.analyze_message(event.text)
            if analysis.get('is_help_request') and not analysis.get('is_ad_or_chat'):
                logger.info(f"✅ اكتشاف طلب مساعدة من {phone}: {event.text[:50]}...")
                # نقل الرسالة للجروب المستهدف
                try:
                    await client.forward_messages(Config.TARGET_GROUP_ID, event.message)
                except Exception as e:
                    logger.error(f"❌ خطأ في تحويل الرسالة: {e}")

        await client.start(phone=phone)
        self.clients.append(client)
        logger.info(f"🚀 حساب المراقبة {phone} متصل الآن")

    async def start_advertiser(self, account_data):
        """تشغيل حساب نشر إعلانات"""
        phone, api_id, api_hash, session_name = account_data[1], account_data[2], account_data[3], account_data[4]
        client = TelegramClient(f"sessions/{session_name}", api_id, api_hash)
        await client.start(phone=phone)
        self.clients.append(client)
        logger.info(f"📢 حساب الإعلانات {phone} متصل الآن")
        
        # مهمة دورية لنشر الإعلانات
        asyncio.create_task(self.ad_scheduler(client))

    async def ad_scheduler(self, client):
        """مجدول الإعلانات لهذا الحساب"""
        while True:
            tasks = self.db.get_ad_tasks()
            for task in tasks:
                msg, groups = task[1], eval(task[2]) # groups is a list
                for group in groups:
                    try:
                        await client.send_message(group, msg)
                        logger.info(f"✅ تم نشر إعلان في {group}")
                        await asyncio.sleep(60) # تأخير بين الجروبات لتجنب الحظر
                    except Exception as e:
                        logger.error(f"❌ خطأ في نشر إعلان: {e}")
                
                await asyncio.sleep(task[3] * 60) # الانتظار حسب الفاصل الزمني للمهمة
            await asyncio.sleep(300) # فحص المهام الجديدة كل 5 دقائق

    async def run_all(self):
        accounts = self.db.get_accounts()
        tasks = []
        for acc in accounts:
            if acc[5] == 'worker':
                tasks.append(self.start_worker(acc))
            elif acc[5] == 'advertiser':
                tasks.append(self.start_advertiser(acc))
        
        if tasks:
            await asyncio.gather(*tasks)
            # البقاء في حالة تشغيل
            while True:
                await asyncio.sleep(3600)
        else:
            logger.warning("⚠️ لا توجد حسابات مضافة في قاعدة البيانات!")

if __name__ == '__main__':
    manager = MultiAccountManager()
    try:
        asyncio.run(manager.run_all())
    except KeyboardInterrupt:
        pass
