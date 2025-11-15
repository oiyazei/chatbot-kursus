import re

def normalize_slang(text):
    norm = {
        r"(gk|ga|nggak+|tdk)": "tidak",
        r"(aja|aj|sj)": "saja",
        r"(blm|blum|blom)": "belum",
        r"(udh|udha)": "sudah",
        r"(dr|dri)": "dari",
        r"(sy|sya|gw|ak|akuh|aq|gue)": "saya",
        r"(tp|tpi|tapikan)": "tapi",
        r"(pl|pricelist|price)": "harga",
        r"(brp|brpa|brapa|bro|brpaan|berapaan)": "berapa",
        r"(utk)": "untuk",
        r"(kls|klas)": "kelas",
        r"(kk|bg|teh)": "kak",
        r"(bhs|bhasa|bhsa)": "bahasa",
        r"(klo|kl)": "kalau",
        r"(apk|software|apl|aplk)": "aplikasi",
        r"(bljr|beelajar|bl+e*a*j+ar*)": "belajar",
        r"(spt)": "seperti",
        r"(spek)": "spesifikasi",
        r"(jg)": "juga",
        r"(blh|leh)": "boleh",
        r"(gni)": "begini",
        r"(paid)": "berbayar",
        r"(sblnny|sbln)": "sebulan",
        r"(tlong|tlg)": "tolong",
        r"(jgn|jangn)": "jangan",
        r"(nuhun|mksh|tks|tq|thx)": "terimakasih",
        r"(perbln)": "perbulan",
        r"(ank)": "anak",
        r"(bkin|bwt|bikn)": "buat",
        r"(dri|dr)": "dari",
        r"(info|ingfo|inf)": "informasi",
        r"(wa|wasap|watsap)": "whatsapp",
        r"(no|nomer|nmr|nmer)": "nomor",
        r"(emg)": "emang",
        r"(sppx)": "membayar",
        r"(japri|chet)": "chat",
        r"(jdwlnya|jdwl|jadwl)": "jadwal",
        r"(pls)": "mohon",
        r"(min)": "admin",
        r"(yg)": "yang",
        r"(dftr|dftsr|daftr)": "daftar",
        r"(byr|byar|bayr|bsyar)": "bayar",
        r"(tarif|fee|pembiayaan|biyaya)": "biaya",
        r"(math|mtk)": "matematika",
        r"(eng|ingris|ing)": "inggris",
        r"(course|bootcamp|khursus|les)": "kursus",
        r"(basic|zero)": "dasar",
        r"(friendly|easy)": "mudah",
        r"(koding|codiing|codng)": "coding",
        r"(qr)": "qris",
        r"(tools)": "alat",
        r"(benefit)": "keuntungan",
        r"(beginner|beginer)": "pemula",
        r"(sertif)": "sertifikat",
        r"(worth)": "layak",
        r"(tutor|mentor)": "guru",
        r"(recording)": "rekaman",
        r"(booklet)": "buku",
        r"(hisensi)": "hisensei",
        r"p?rog?ra?m+e*r+": "programmer",
        r"(pembljrn|pmbljrn)": "pembelajaran",
        r"(byr|pmbayaran|penbayaran|pmbyran|pmbsyaran)": "pembayaran",
        r"(mtode|metod)": "metode",
        r"(desin|desayn)": "desain",
        r"(join|ikut)": "gabung",
        r"(py+th?o+n+)": "python",
        r"(gmn|gmna|g+mn*a*)": "gimana",
    }

    if not isinstance(text, str):
        return ""

    text = re.sub(r"[^\w\s]", "", text)
    words = text.lower().split()
    normalized = []

    for word in words:
        replaced = False
        for pattern, replacement in norm.items():
            if re.fullmatch(pattern, word):
                normalized.append(replacement)
                replaced = True
                break
        if not replaced:
            normalized.append(word)

    return " ".join(normalized)
