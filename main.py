import json
import torch
import re
from transformers import BertTokenizer, BertForSequenceClassification
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def normalize_slang(text):
    norm = {
        "gk": "tidak", "ga": "tidak", "nggak": "tidak", "tdk": "tidak",
        "aja": "saja", "blm": "belum", "udh": "sudah", "dr": "dari",
        "sm": "sama", "sy": "saya", "tp": "tapi", "pl": "harga",
        "brp": "berapa", "utk": "untuk", "kls": "kelas", "brpa": "berapa",
        "kk": "kakak", "sya": "saya", "brapa": "berapa", "bhs": "bahasa",
        "klo": "kalau", "apk": "aplikasi", "bljr": "belajar", "spt": "seperti",
        "spek": "spesifikasi", "gmn": "gimana", "leptop": "laptop",
        "dmn": "dimana", "gmna": "gimana", "jg": "juga", "blh": "boleh",
        "gni": "begini", "paid": "berbayar", "sblnny": "sebulannya",
        "tlong": "tolong", "jgn": "jangan", "donk": "dong", "nuhun": "terimakasih",
        "perbln": "perbulan", "teh": "kak", "gw": "saya", "bg": "kak",
        "bs": "bisa", "ank": "anak", "bkin": "buat", "dri": "dari",
        "info": "informasi", "si": "sih", "wa": "whatsapp", "no": "nomor",
        "emg": "emang", "bwt": "buat", "bro": "berapa", "sppx": "membayar",
        "mksh": "terimakasih", "tks": "terimakasih", "ny": "nya",
        "mtk": "matematika", "japri": "chat", "jdwlnya": "jadwalnya",
        "pls": "please", "min": "admin", "nggk": "tidak", "yg": "yang",
        "dftr": "daftar", "byr": "bayar", "byar": "bayar", "bljar": "belajar",
        "pricelist": "harga", "design": "desain", "tarif": "biaya", "fee": "biaya",
        "math": "matematika", "eng": "inggris", "course": "kursus", "basic": "dasar",
        "zero": "nol", "friendly": "mudah", "koding": "coding", "qr": "qris",
        "tools": "alat", "benefit": "keuntungan", "nomer": "nomor",
        "beginner": "pemula", "sertif": "sertifikat", "bootcamp": "kursus",
        "beginer": "pemula", "ingfo": "info", "worth": "layak", "khursus": "kursus",
        "tutor": "guru", "tq": "terimakasih", "join": "gabung", "beelajar": "belajar",
        "mentor": "guru", "recording": "rekaman", "booklet": "buku", "codiing": "coding",
        "software": "aplikasi", "leh": "boleh", "hisensi": "hisensei", "programer": "programmer", "pembljrn": "pembelajaran",
        "pembyran": "pembayaran", "pembyarn" : "pembayaran",
    }

    if not isinstance(text, str):
        return ""
    
    text = re.sub(r"[^\w\s]", "", text)  # hapus semua tanda baca kecuali huruf dan spasi
    words = text.lower().split()
    normalized = [norm.get(w, w) for w in words if w]
    return " ".join(normalized)

class IndoBERTTelegramBot:
    def __init__(self, token, model_path, label_json_path):
        self.token = token
        self.model_path = model_path
        self.label_map = self.load_label_map(label_json_path)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

        self.updater = Updater(token=self.token, use_context=True)
        self.dp = self.updater.dispatcher

        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.predict_intent))

    def load_label_map(self, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        id2label = {int(k): v for k, v in data["id2label"].items()}
        return id2label

    def start(self, update, context):
        update.message.reply_text("Hai! Kirim pertanyaanmu, dan aku akan prediksi intent-nya.")

    def predict_intent(self, update, context):
        raw_text = update.message.text
        cleaned_text = normalize_slang(raw_text)

        inputs = self.tokenizer(cleaned_text, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class = int(torch.argmax(logits, dim=1).item())
            label = self.label_map.get(predicted_class, "intent_tidak_dikenal")

        update.message.reply_text(f"Prediksi intent: {label}")
    
        # Debug output
        print(f"[RAW] {raw_text}")
        print(f"[CLEANED] {cleaned_text}")
        print(f"[PREDICTED CLASS] {predicted_class} -> {label}")

    def run(self):
        print("Bot is running...")
        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    TOKEN = "8017210730:AAFrIkZ80tbOy5E8uVB_XZUt9qorjw94yWU"
    MODEL_PATH = "pixelbitter/indobert_89"
    LABEL_JSON_PATH = "indobert_newest_label.json"

    bot = IndoBERTTelegramBot(TOKEN, MODEL_PATH, LABEL_JSON_PATH)
    bot.run()
