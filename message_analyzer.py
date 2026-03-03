"""
محلل متقدم لرسائل تيليجرام
Advanced Telegram Message Analyzer
"""

import re
from typing import Tuple, List, Optional


class MessageAnalyzer:
    """فئة محلل الرسائل"""
    
    def __init__(self):
        # قوائم الكلمات المفتاحية لكل نوع خدمة
        self.service_keywords = {
            'شرح': [
                'شرح', 'اشرح', 'فهم', 'تفسير', 'تحليل', 'توضيح', 
                'بيان', 'شرحت', 'يفهم', 'مفهوم', 'توضيحات',
                'شرحها', 'اشرحها', 'فهمتها', 'تفسيرها'
            ],
            'تقارير': [
                'تقرير', 'تقارير', 'تلخيص', 'ملخص', 'تكليف', 
                'تكاليف', 'تلاخيص', 'تقاريري', 'ملخصات',
                'تكليفي', 'تكلفة', 'يحتاج تقرير'
            ],
            'واجبات': [
                'واجب', 'واجبات', 'بحث', 'بحوث', 'مشروع', 
                'مشاريع', 'بروجكت', 'أسايمنت', 'assignment', 
                'project', 'واجبي', 'بحثي', 'مشروعي',
                'home', 'work', 'homework'
            ],
            'عروض': [
                'برزنتيشن', 'عرض', 'بوربوينت', 'presentation', 
                'powerpoint', 'سلايدات', 'شرائح', 'عرضي',
                'برزنتيشن', 'ppt', 'slide'
            ],
            'تصاميم': [
                'تصميم', 'تصاميم', 'غرافيك', 'logo', 'banner', 
                'بوستر', 'بروشور', 'مطوية', 'انفوجرافيك', 
                'autocad', '2d', '3d', 'كورل', 'فوتوشوب',
                'photoshop', 'illustrator', 'دزاين'
            ],
            'خرائط': [
                'خريطة ذهنية', 'mind map', 'خرائط ذهنية', 
                'مخطط', 'diagram', 'schema', 'mindmap'
            ],
            'ماجستير': [
                'ماجستير', 'رسالة ماجستير', 'بحث ماجستير', 
                'thesis', 'master thesis', 'ماستر'
            ],
            'تخرج': [
                'مشروع تخرج', 'graduation project', 'تخرج',
                'project تخرج', 'مشروع تخرجي'
            ],
            'طبي': [
                'تقرير طبي', 'أجازة مرضية', 'شهادة مرضية', 
                'مرافق مريض', 'مشهد مراجعة', 'شهادة طبية',
                'مراجعة طبية', 'تقرير طبي'
            ],
            'ريبورت': [
                'ريبورت', 'report', 'تقرير', 'تقارير'
            ]
        }
        
        # أنماط إضافية للتحليل
        self.request_patterns = [
            r'محتاج.*مساعدة',
            r'من يساعدني',
            r'أحد يقدر.*يخدم',
            r'ممكن.*تساعد',
            r'عندكم.*?',
            r'من عنده.*?',
            r'أحد عنده.*?',
            r'هل يوجد.*?',
            r'أريد.*?',
            r'ابغى.*?',
        ]
        
        # كلمات مؤكدة للطلب
        self.request_indicators = [
            'محتاج', 'من يساعدني', 'أحد يقدر', 'ممكن', 
            'عندكم', 'من عنده', 'هل يوجد', 'أريد', 'ابغى',
            'أحتاج', 'طلب', 'طلبت', 'رجاء', 'ساعدني', 'ساعدوني'
        ]
        
    def clean_text(self, text: str) -> str:
        """تنظيف النص من الرموز الزائدة"""
        # إزالة الرموز الزائدة مع الحفاظ على المسافات
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        # إزالة المسافات المتعددة
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    def extract_services(self, text: str) -> List[str]:
        """استخراج أنواع الخدمات من النص"""
        found_services = []
        cleaned_text = self.clean_text(text).lower()
        
        for service, keywords in self.service_keywords.items():
            for keyword in keywords:
                if keyword.lower() in cleaned_text:
                    found_services.append(service)
                    break
                    
        return list(set(found_services))
        
    def is_help_request(self, text: str) -> Tuple[bool, Optional[List[str]]]:
        """
        تحديد إذا كانت الرسالة طلب مساعدة
        
        العوائد:
            (bool): هل هي طلب مساعدة
            (list): قائمة الخدمات المطلوبة (إن وجدت)
        """
        if not text or len(text) < 10:
            return False, None
            
        cleaned_text = self.clean_text(text).lower()
        
        # استخراج الخدمات المطلوبة
        services = self.extract_services(text)
        
        # إذا وجدت خدمات، فهو طلب مساعدة
        if services:
            return True, services
            
        # البحث عن أنماط طلبات المساعدة
        for pattern in self.request_patterns:
            if re.search(pattern, cleaned_text):
                return True, ['مساعدة عامة']
                
        # البحث عن مؤشرات الطلب
        for indicator in self.request_indicators:
            if indicator in cleaned_text:
                return True, ['مساعدة عامة']
                
        return False, None
        
    def analyze_message(self, text: str) -> dict:
        """
        تحليل شامل للرسالة
        
        العوائد:
            dict: يحتوي على:
                - is_help_request: هل هي طلب مساعدة
                - services: الخدمات المطلوبة
                - confidence: نسبة الثقة (0-100)
                - keywords: الكلمات المفتاحية الموجودة
        """
        result = {
            'is_help_request': False,
            'services': [],
            'confidence': 0,
            'keywords': []
        }
        
        if not text or len(text) < 10:
            return result
            
        cleaned_text = self.clean_text(text)
        
        # استخراج الخدمات
        services = self.extract_services(text)
        
        if services:
            result['is_help_request'] = True
            result['services'] = services
            
            # حساب نسبة الثقة بناءً على عدد الخدمات
            base_confidence = min(len(services) * 20, 80)
            
            # إضافة الثقة بناءً على مؤشرات الطلب
            for indicator in self.request_indicators:
                if indicator in cleaned_text.lower():
                    base_confidence += 10
                    
            result['confidence'] = min(base_confidence, 100)
            
            # استخراج الكلمات المفتاحية الموجودة
            result['keywords'] = self._extract_found_keywords(cleaned_text)
            
        return result
        
    def _extract_found_keywords(self, text: str) -> List[str]:
        """استخراج الكلمات المفتاحية الموجودة في النص"""
        found_keywords = []
        text_lower = text.lower()
        
        for keywords in self.service_keywords.values():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found_keywords.append(keyword)
                    
        return list(set(found_keywords))
        
    def get_service_type(self, text: str) -> str:
        """
        تحديد نوع الخدمة الرئيسية المطلوبة
        
        العوائد:
            str: اسم الخدمة أو 'مساعدة عامة'
        """
        services = self.extract_services(text)
        
        if services:
            # إرجاع الخدمة الأولى
            return services[0]
            
        return 'مساعدة عامة'


# استخدام المثال
if __name__ == '__main__':
    analyzer = MessageAnalyzer()
    
    # اختبار
    test_messages = [
        "السلام عليكم، محتاج مساعدة في واجب الرياضيات",
        "من عنده تقرير للفيزياء؟",
        "أحد يقدر يساعدني في مشروع التخرج",
        "ابغى تصميم بوستر لمشروعي",
        "مرحباً جميعاً، كيف حالكم؟"
    ]
    
    for msg in test_messages:
        result = analyzer.analyze_message(msg)
        print(f"\nالرسالة: {msg}")
        print(f"طلب مساعدة: {result['is_help_request']}")
        print(f"الخدمات: {result['services']}")
        print(f"نسبة الثقة: {result['confidence']}%")
        print(f"الكلمات المفتاحية: {result['keywords']}")