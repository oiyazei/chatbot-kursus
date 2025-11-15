import re

# Fallback keyword detection
FALLBACK_KEYWORDS = ["bingung", "ga ngerti", "tidak tahu", "tidak paham"]
FALLBACK_OUTOFSCOPE = ["buatkan", "buatlah", "contohkan", "contoh", "selesaikan", "rumus", "makan", "tuliskan", "namamu", "tulis", "mengapa", "kenapa", "wanjir", "anjir", "anj", "sayang"]
# Rule mapping keyword ke intent override
INTENT_KEYWORDS = {
    "pembayaran": ["kredit", "debit"],
    "aplikasi": ["lms"],
}

def detect_fallback(user_text: str):
    lower_text = user_text.lower()

    # 1. Fallback jika mengandung kata bantu atau membingungkan
    if any(k in lower_text for k in FALLBACK_KEYWORDS):
        return "umum"
    if any(k in lower_text for k in FALLBACK_OUTOFSCOPE):
        return "outofscope"

    # 2. Fallback jika input terlalu pendek
    if len(lower_text.strip().split()) < 2:
        return "outofscope"

    return None

def rule_based_intent_override(user_text: str, model_intent: str):
    lower_text = user_text.lower()
    
    # 3. Cek apakah ada keyword yang cocok dengan intent tertentu
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            # exact match atau kata turunan
            if re.search(rf"\b{kw}\w*\b", lower_text):
                if intent != model_intent:
                    return intent  

    return model_intent

def resolve_intent(user_text: str, model_intent: str):
    """
    Final resolver: mendahulukan override berbasis keyword
    sebelum mengecek apakah perlu fallback.
    """
    lower_text = user_text.lower()

    # Langkah 1: cek override keyword
    final_intent = rule_based_intent_override(lower_text, model_intent)

    # Langkah 2: fallback hanya kalau tidak berubah
    fallback = detect_fallback(lower_text)
    if fallback and final_intent == model_intent:
        return fallback

    return final_intent


def hisensei_fix(user_input_lower):
    """
    Aturan STRIKT:
    - Harus ada: "info" dan "kursus" dan salah satu dari: "mtk", "inggris", "hisensei"
    - Kalau juga ada "biaya" / "harga" → intent = biaya_hisensei
    - Kalau tidak, intent = kursus_hisensei
    """
    hisensei_keywords = ["mtk", "matematika", "inggris", "hisensei", "bimbel"]
    
    if all(k in user_input_lower for k in ["info", "kursus"]) and any(k in user_input_lower for k in hisensei_keywords):
        return "kursushisensei"
    
    return None






