import json
import torch
import re
from transformers import BertTokenizer, BertForSequenceClassification
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dst import DialogManager  
from fallback import resolve_intent, hisensei_fix
from normalizer import normalize_slang

class IndoBERTBot:
    def __init__(self, token, model_path, label_json_path, answer_json_path):
        self.token = token
        self.dialog = DialogManager(answer_json_path)
        self.label_map = self.load_label_map(label_json_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

        self.updater = Updater(token=self.token, use_context=True)
        self.dp = self.updater.dispatcher

        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))

    def load_label_map(self, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        return {int(k): v for k, v in data["id2label"].items()}

    def start(self, update, context):
        update.message.reply_text(
            "Hai! Selamat datang di Chatbot Akademik! Aku adalah pusat Informasi terkait : \n\n"
            "- Info Coding, Design, Hisensei (Inggris & Matematika) di Akademi\n\n"
            "- Info terkait Pendaftaran / Trial Class, Metode Pembayaran, Harga Kursus, Pembelajaran, Aplikasi yang digunakan hingga Usia Peserta. \n\n"
            "Kamu bisa LANGSUNG kirim pertanyaan kamu, ya! seperti : \n"
            "'Gimana Pendaftaran kursusnya, kak?'\n"
            "'Metode pembayarannya seperti apa?\n"
            "'Apa itu Coding?'\n"
            "'Berapa biaya kursus?'\n"
            "Aku akan berusaha menjawab ^^ \n\n"
            "BATASAN : \n\n"
            "- Chatbot belum bisa menjawab sapaan dan terimakasih, serta pertanyaan 'mengapa', 'kenapa'\n"
            "- Chatbot HANYA bisa menjawab pertanyaan seputar akademi, seperti : 'Batasan Usia Peserta' / 'Bagaimana cara daftar' / 'metode pembayaran bagaimana', \n\n"
            "Jadi kamu bisa kirim langsung pertanyaanmu ya, pakai bahasa informal juga boleh! :D"
        )

    def predict_intent(self, text):
        cleaned = normalize_slang(text)
        inputs = self.tokenizer(cleaned, return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits
            pred_class = int(torch.argmax(logits, dim=1).item())
            return self.label_map.get(pred_class, "intent_tidak_dikenal")

    def handle_message(self, update, context):
        user_id = update.message.chat_id
        user_input = update.message.text
        cleaned_input = normalize_slang(user_input)
        user_input_lower = cleaned_input.lower()

        last_intent = self.dialog.get_last_intent(user_id)
        intent = None

        # === Cek dulu rule khusus hisensei ===
        rule_intent = hisensei_fix(user_input_lower)
        if rule_intent:
            intent = rule_intent

        elif last_intent == "biaya":
            if len(user_input_lower.split()) <= 3 and "coding" in user_input_lower:
                intent = "biaya_coding"
            elif len(user_input_lower.split()) <= 3 and ("desain" in user_input_lower or "design" in user_input_lower):
                intent = "biaya_design"
            elif len(user_input_lower.split()) <= 3 and any(k in user_input_lower for k in ["hisensei", "inggris", "mtk", "matematika", "bimbel"]):
                intent = "biaya_hisensei"
            else:
                model_intent = self.predict_intent(user_input)
                intent = resolve_intent(user_input, model_intent)
        else:
            model_intent = self.predict_intent(user_input)
            intent = resolve_intent(user_input, model_intent)

        self.dialog.update_state(user_id, intent)
        response = self.dialog.get_response(intent)
        update.message.reply_text(response)

    def run(self):
        print("Bot is running...")
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    TOKEN = "8017210730:AAFrIkZ80tbOy5E8uVB_XZUt9qorjw94yWU"
    MODEL_PATH = "pixelbitter/indobert_89"
    LABEL_JSON_PATH = "indobert_newest_label.json"
    ANSWER_JSON_PATH = "answer.json"

    bot = IndoBERTBot(TOKEN, MODEL_PATH, LABEL_JSON_PATH, ANSWER_JSON_PATH)
    bot.run()
