import re
import json
import asyncio
from typing import Tuple, List, Optional
from openai import OpenAI
import time

class MessageAnalyzerV2:
    def __init__(self, db=None):
        self.db = db
        # الكلمات المفتاحية الأساسية + الكلمات الجديدة المطلوبة
        self.request_indicators = [
            'محتاج', 'من يساعدني', 'أحد يقدر', 'ممكن', 
            'عندكم', 'من عنده', 'هل يوجد', 'أريد', 'ابغى',
            'أحتاج', 'طلب', 'طلبت', 'رجاء', 'ساعدني', 'ساعدوني',
            'ابي', 'ابغا', 'حد', 'احد', 'يحل', 'يسوي', 'مساعده', 'يساعد'
        ]
        
        # إضافة الكلمات المخصصة من قاعدة البيانات إذا وجدت
        if self.db:
            custom = self.db.get_keywords()
            self.request_indicators.extend(custom)
            self.request_indicators = list(set(self.request_indicators))

        # إعداد عميل OpenAI (يستخدم gpt-4.1-mini للسرعة والدقة)
        self.client = OpenAI()

    def clean_text(self, text: str) -> str:
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    async def analyze_with_ai(self, text: str) -> dict:
        """تحليل الرسالة باستخدام الذكاء الاصطناعي في أقل من 3 ثوانٍ"""
        start_time = time.time()
        
        prompt = f"""
        حلل الرسالة التالية من جروب تيليجرام وصنفها:
        الرسالة: "{text}"
        
        المطلوب:
        1. هل هي طلب مساعدة حقيقي (حل واجب، شرح، بحث، تصميم، إلخ)؟
        2. هل هي إعلان أو سبام أو دردشة عادية؟
        
        أجب بتنسيق JSON فقط كالتالي:
        {{
            "is_help_request": true/false,
            "is_ad_or_chat": true/false,
            "confidence": 0-100,
            "reason": "سبب التصنيف باختصار"
        }}
        """
        
        try:
            # استخدام gpt-4.1-mini لضمان السرعة (أقل من 3 ثوانٍ)
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "أنت خبير في تحليل الرسائل وتصنيفها بدقة وسرعة عالية."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                timeout=2.5 # تحديد مهلة زمنية صارمة
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # التأكد من عدم تجاوز الوقت
            duration = time.time() - start_time
            if duration > 3:
                print(f"⚠️ تحذير: التحليل استغرق {duration:.2f} ثانية")
                
            return result
        except Exception as e:
            print(f"❌ خطأ في تحليل AI: {e}")
            # العودة للتحليل التقليدي في حال فشل AI
            return self.fallback_analysis(text)

    def fallback_analysis(self, text: str) -> dict:
        """تحليل احتياطي يعتمد على الكلمات المفتاحية"""
        cleaned_text = self.clean_text(text).lower()
        is_help = any(indicator in cleaned_text for indicator in self.request_indicators)
        
        return {
            "is_help_request": is_help,
            "is_ad_or_chat": False,
            "confidence": 70 if is_help else 0,
            "reason": "Keyword matching (fallback)"
        }

    async def analyze_message(self, text: str) -> dict:
        """المعالج الرئيسي للتحليل"""
        if not text or len(text) < 5:
            return {"is_help_request": False, "is_ad_or_chat": False, "confidence": 0}

        # الخطوة 1: فحص سريع بالكلمات المفتاحية (لتوفير تكلفة AI للرسائل البعيدة تماماً)
        cleaned_text = self.clean_text(text).lower()
        potential_help = any(indicator in cleaned_text for indicator in self.request_indicators)
        
        if not potential_help:
            return {"is_help_request": False, "is_ad_or_chat": False, "confidence": 0}

        # الخطوة 2: التحليل العميق بالذكاء الاصطناعي
        return await self.analyze_with_ai(text)
