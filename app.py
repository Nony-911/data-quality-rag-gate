import pandas as pd
from datetime import datetime

# ==========================================
# 1. Data Quality Gate (محرك فحص الجودة)
# ==========================================
class DataQualityEngine:
    """
    محرك فحص جودة البيانات المعتمد وفق معايير SDAIA Data Governance:
    - Completeness (الاكتمال)
    - Accuracy (الدقة)
    - Validity (الصلاحية وجمع الـ Spam)
    """
    def __init__(self, raw_data: list):
        self.df = pd.DataFrame(raw_data)
        self.passed_records = []
        self.quarantine_zone = []

    def run_pipeline(self):
        print("==================================================")
        print(f"🚀 [SDAIA DQ Gate] بدء تشغيل أنبوب الجودة: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("==================================================\n")

        for idx, row in self.df.iterrows():
            rejection_reasons = []

            # 1. Completeness Check
            if pd.isna(row.get("user_email")) or not str(row.get("user_email")).strip():
                rejection_reasons.append("Completeness Failure: Missing user email")

            # 2. Accuracy Check
            rating = row.get("rating")
            if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
                rejection_reasons.append(f"Accuracy Failure: Invalid rating ({rating})")

            # 3. Validity Check (Spam Filter)
            review_text = str(row.get("review", ""))
            spam_keywords = ["إعلان", "اشترك", "رابط", "http"]
            if any(keyword in review_text for keyword in spam_keywords):
                rejection_reasons.append("Validity Failure: Spam detected")

            # Routing Logic
            if rejection_reasons:
                quarantine_entry = row.to_dict()
                quarantine_entry["rejection_reasons"] = " | ".join(rejection_reasons)
                self.quarantine_zone.append(quarantine_entry)
                print(f"[❌ QUARANTINE] السجل {row['product_id']} تم عزله: {rejection_reasons[0]}")
            else:
                self.passed_records.append(row.to_dict())
                print(f"[✅ PASSED] السجل {row['product_id']} اجتاز فحص الجودة بنجاح.")

        return pd.DataFrame(self.passed_records), pd.DataFrame(self.quarantine_zone)

# ==========================================
# 2. RAG Pipeline (استرجاع المحتوى المفلتر)
# ==========================================
class SimpleRAGPipeline:
    """
    نظام RAG يستقبل البيانات النظيفة فقط من الـ DQ Gate
    ويقوم ببناء الفهرس والبحث في التقييمات المقبولة.
    """
    def __init__(self, clean_df: pd.DataFrame):
        self.knowledge_base = clean_df

    def query(self, search_term: str):
        print(f"\n🔍 [RAG Search Query]: '{search_term}'")
        if self.knowledge_base.empty:
            return "قاعدة البيانات المعرفية فارغة."
        
        # استرجاع المحتوى المطابق من البيانات النظيفة
        results = self.knowledge_base[self.knowledge_base['review'].str.contains(search_term, na=False)]
        
        if not results.empty:
            print(f"✨ [RAG Response]: تم العثور على {len(results)} تقييمات موثوقة في قاعدة المعرفة:")
            for idx, row in results.iterrows():
                print(f"   - المنتج {row['product_id']} (تقييم: {row['rating']}/5): \"{row['review']}\"")
        else:
            print("⚠️ [RAG Response]: لم يتم العثور على نتائج مطابقة في البيانات المعتمدة.")

# ==========================================
# 3. Execution (التنفيذ الشامل)
# ==========================================
if __name__ == "__main__":
    # dataset مدخلة محاكاة
    raw_dataset = [
        {"product_id": "P101", "review": "سماعة ممتازة وصوتها واضح جداً", "rating": 5, "user_email": "norah@example.com"},
        {"product_id": "P102", "review": "شاحن بطيء جداً ولا يعجبني", "rating": 1, "user_email": "ahmed@example.com"},
        {"product_id": "P103", "review": "إعلان سبام اشتروا الآن عبر هذا الرابط!!", "rating": -1, "user_email": "bot@spam.com"},
        {"product_id": "P104", "review": "منتج جيد وعملي", "rating": 4, "user_email": None},
        {"product_id": "P105", "review": "سماعة بلوتوث جودتها متوسطة", "rating": 3, "user_email": "sara@example.com"}
    ]

    # Step 1: Run Data Quality Gate
    dq_engine = DataQualityEngine(raw_dataset)
    clean_df, quarantine_df = dq_engine.run_pipeline()

    # Step 2: Feed Clean Data into RAG Pipeline
    print("\n==================================================")
    print("🧠 تغذية نظام الـ RAG بالبيانات المعتمدة فقط (Quality-Filtered RAG)")
    print("==================================================")
    rag = SimpleRAGPipeline(clean_df)
    
    # Step 3: RAG Retrieval Test
    rag.query("سماعة")