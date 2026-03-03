@echo off
REM سكريبت تشغيل البوت على Windows

echo 🚀 بدء تشغيل بوت تحليل طلبات المساعدة الطلابية...
echo ==================================================

REM التحقق من وجود Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت. يرجى تثبيته أولاً.
    pause
    exit /b 1
)

REM التحقق من وجود ملف .env
if not exist .env (
    echo ⚠️  ملف .env غير موجود.
    echo 📋 جاري نسخ ملف .env.example...
    copy .env.example .env >nul
    echo ✏️  يرجى تعديل ملف .env وإدخال بياناتك الحقيقية
    echo    notepad .env
    pause
    exit /b 1
)

REM تثبيت المتطلبات
echo 📦 التحقق من المتطلبات...
pip install -r requirements.txt -q

REM تشغيل البوت
echo 🤖 بدء تشغيل البوت...
python student_help_bot.py

pause