#!/bin/bash
# سكريبت تشغيل البوت على Linux/Mac

echo "🚀 بدء تشغيل بوت تحليل طلبات المساعدة الطلابية..."
echo "=================================================="

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت. يرجى تثبيته أولاً."
    exit 1
fi

# التحقق من وجود ملف .env
if [ ! -f .env ]; then
    echo "⚠️  ملف .env غير موجود."
    echo "📋 جاري نسخ ملف .env.example..."
    cp .env.example .env
    echo "✏️  يرجى تعديل ملف .env وإدخال بياناتك الحقيقية"
    echo "   nano .env"
    exit 1
fi

# تثبيت المتطلبات
echo "📦 التحقق من المتطلبات..."
pip3 install -r requirements.txt -q

# تشغيل البوت
echo "🤖 بدء تشغيل البوت..."
python3 student_help_bot.py