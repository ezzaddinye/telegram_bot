from telethon import TelegramClient, events, Button
import asyncio
import os
from database import Database

class AdminPanel:
    def __init__(self, bot_token, api_id, api_hash, admin_id):
        self.client = TelegramClient('admin_bot', api_id, api_hash).start(bot_token=bot_token)
        self.db = Database()
        self.admin_id = int(admin_id)
        self.setup_handlers()

    def setup_handlers(self):
        @self.client.on(events.NewMessage(pattern='/start', from_users=self.admin_id))
        async def start_handler(event):
            await self.show_main_menu(event)

        @self.client.on(events.CallbackQuery())
        async def callback_handler(event):
            data = event.data.decode()
            if data == 'manage_accounts':
                await self.show_accounts_menu(event)
            elif data == 'manage_ads':
                await self.show_ads_menu(event)
            elif data == 'manage_keywords':
                await self.show_keywords_menu(event)
            elif data == 'main_menu':
                await self.show_main_menu(event, edit=True)

    async def show_main_menu(self, event, edit=False):
        buttons = [
            [Button.inline("📱 إدارة الحسابات", b"manage_accounts")],
            [Button.inline("📢 إدارة الإعلانات", b"manage_ads")],
            [Button.inline("🔑 الكلمات المفتاحية", b"manage_keywords")],
            [Button.inline("📊 الإحصائيات", b"stats")]
        ]
        text = "👋 مرحباً بك في لوحة تحكم مدير البوت\nاختر من القائمة أدناه:"
        if edit:
            await event.edit(text, buttons=buttons)
        else:
            await event.respond(text, buttons=buttons)

    async def show_accounts_menu(self, event):
        accounts = self.db.get_accounts()
        text = "📱 **قائمة الحسابات المضافة:**\n\n"
        if not accounts:
            text += "لا يوجد حسابات مضافة حالياً."
        for acc in accounts:
            text += f"• {acc[1]} ({acc[5]}) - {acc[6]}\n"
        
        buttons = [
            [Button.inline("➕ إضافة حساب", b"add_account")],
            [Button.inline("❌ حذف حساب", b"del_account")],
            [Button.inline("🔙 العودة", b"main_menu")]
        ]
        await event.edit(text, buttons=buttons)

    async def show_ads_menu(self, event):
        text = "📢 **إدارة الإعلانات ونشرها**"
        buttons = [
            [Button.inline("➕ إضافة مهمة إعلانية", b"add_ad")],
            [Button.inline("📋 عرض المهام", b"view_ads")],
            [Button.inline("🔙 العودة", b"main_menu")]
        ]
        await event.edit(text, buttons=buttons)

    async def show_keywords_menu(self, event):
        keywords = self.db.get_keywords()
        text = f"🔑 **الكلمات المفتاحية الحالية:**\n\n{', '.join(keywords) if keywords else 'لا يوجد'}"
        buttons = [
            [Button.inline("➕ إضافة كلمة", b"add_kw")],
            [Button.inline("🔙 العودة", b"main_menu")]
        ]
        await event.edit(text, buttons=buttons)

    def run(self):
        print("🚀 لوحة التحكم تعمل الآن...")
        self.client.run_until_disconnected()

if __name__ == '__main__':
    # هذه القيم يجب أن تؤخذ من .env
    from config import Config
    # ملاحظة: سنحتاج لإضافة ADMIN_BOT_TOKEN و ADMIN_ID إلى ملف .env
    ADMIN_BOT_TOKEN = os.getenv('ADMIN_BOT_TOKEN')
    ADMIN_ID = os.getenv('ADMIN_ID')
    if ADMIN_BOT_TOKEN and ADMIN_ID:
        panel = AdminPanel(ADMIN_BOT_TOKEN, Config.API_ID, Config.API_HASH, ADMIN_ID)
        panel.run()
    else:
        print("❌ يرجى ضبط ADMIN_BOT_TOKEN و ADMIN_ID في ملف .env")
