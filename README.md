# 📋 Kundalik hisobot boti

Boshqarma hodimlari Telegram orqali kundalik hisobot topshiradi, boshqarma boshlig'i esa
ularni bir tugma bilan **Excel (.xlsx)** va **Word (.docx)** formatida yuklab oladi.

---

## 🚀 Ishga tushirish (5 daqiqa)

### 1. Bot yarating
1. Telegramda [@BotFather](https://t.me/BotFather) ni oching → `/newbot`
2. Botga nom va username bering
3. BotFather bergan **tokenni** nusxalab oling

### 2. Sozlamalarni kiriting
`.env.example` faylini **`.env`** deb nusxalang va to'ldiring:

```
BOT_TOKEN=BotFather bergan token
ADMIN_IDS=Boshqarma boshlig'ining Telegram ID raqami
ORG_NAME=Raqamli texnologiyalar boshqarmasi
```

> **Telegram ID ni qanday bilish mumkin?** Botni ishga tushiring va unga `/id` buyrug'ini
> yuboring — bot raqamingizni yozib beradi. O'sha raqamni `ADMIN_IDS` ga qo'ying va botni
> qayta ishga tushiring. (Yoki [@userinfobot](https://t.me/userinfobot) dan bilib oling.)

### 3. Kutubxonalarni o'rnating
```powershell
pip install -r requirements.txt
```

### 4. Botni ishga tushiring
```powershell
python bot.py
```
yoki `start.bat` faylini ikki marta bosing.

Bot ishlab turgan vaqtdagina hisobot qabul qiladi — kompyuter yoki server o'chmasligi kerak.

---

## 🌐 Til

Bot **o'zbek** va **rus** tillarida ishlaydi. Birinchi `/start` da til so'raladi:

```
🌐 Tilni tanlang / Выберите язык
   [🇺🇿 O'zbekcha]   [🇷🇺 Русский]
```

Tanlov har bir foydalanuvchi uchun alohida saqlanadi — bir hodim o'zbekcha, boshqasi ruscha
ishlatishi mumkin. Keyin **«🌐 Til»** tugmasi yoki `/til` buyrug'i orqali o'zgartiriladi.
Excel va Word hujjatlari ham boshliq tanlagan tilda shakllanadi (ustun nomlari, sanalar, imzo joyi).

Barcha matnlar [i18n.py](i18n.py) faylida — tarjimani o'zgartirish yoki yangi til qo'shish shu yerda.

## 🔢 Tabel raqami — parol o'rnida

Boshqarmaning shtat ro'yxati **`staff.json`** faylida: **tabel raqami — F.I.Sh. — lavozim**.
Bu fayl GitHubga tushmaydi (`.gitignore` da) — hodimlarning shaxsiy ma'lumotlari va
kirish raqamlari ochiq qolmasligi uchun. Namuna: [staff.example.json](staff.example.json).

Hodim `/start` bosgach faqat **tabel raqamini** kiritadi. Bot ro'yxatdan uni topib beradi:

```
🔎 Topildi
👤 F.I.Sh.: FAMILIYA ISM SHARIF
💼 Lavozim: Yetakchi muhandis
🔢 Tabel №: 1234
        Bu sizmi?
   [✅ Ha, bu menman]  [🔁 Yo'q, boshqa raqam]
```

Tasdiqlagach — **F.I.Sh. va lavozim avtomatik biriktiriladi** va hodim darhol hisobot
to'ldirishga o'tadi. Hech narsa yozib o'tirmaydi.

- Ro'yxatda yo'q raqam qabul qilinmaydi — begona odam ro'yxatdan o'ta olmaydi
- Bitta tabel raqamini faqat bitta Telegram akkaunt egallaydi
- `3` deb kiritilsa ham `0003` topiladi (boshidagi nollar shart emas)

**Yangi hodim qo'shish yoki lavozimni o'zgartirish:** `staff.json` ga qator qo'shing va
botni qayta ishga tushiring:

```json
{"tabel": "1234", "full_name": "YANGIYEV YANGI YANGIVICH", "position": "Texnik qo'llab-quvvatlash mutaxassisi"}
```

Fayl yo'lini `STAFF_FILE` orqali almashtirsa bo'ladi (Render'da Secret File uchun):
`STAFF_FILE=/etc/secrets/staff.json`

## 👨‍💼 Hodim nima qiladi

1. Botga `/start` yuboradi → tilni tanlaydi → **tabel raqamini kiritadi** → tasdiqlaydi.
   Bu bir martalik amal, keyin darhol hisobotga o'tadi.
2. Har kuni **«📝 Hisobot topshirish»** tugmasini bosadi va 3 ta savolga javob yozadi:
   - 1️⃣ Bugun bajarilgan ishlar
   - 2️⃣ Muammo va takliflar *(o'tkazib yuborish mumkin)*
   - 3️⃣ Ertangi rejalar *(o'tkazib yuborish mumkin)*
3. Ko'rib chiqadi va **«✅ Tasdiqlash»** ni bosadi — hisobot boshliqqa darhol yetib boradi.

Qo'shimcha: kecha yoki oxirgi 30 kun ichidagi boshqa sana uchun ham hisobot topshirish mumkin.

### ➕ Kun davomida bir necha marta yozish

Hodim ishni ertalab, tushda va kechqurun — istagan vaqtida yozib borishi mumkin. O'sha kunga
hisobot bo'lsa, bot so'raydi:

```
📄 18.08.2026 uchun hisobotingiz allaqachon bor:
   Serverlar tekshirildi

        Nima qilamiz?
   [➕ Davomini qo'shish]
   [♻️ Butunlay almashtirish]
```

**«➕ Davomini qo'shish»** — yangi matn eskisining ostiga, **vaqt belgisi bilan** qo'shiladi:

```
[09:15]
Serverlar tekshirildi

[13:40]
VIP kassa internet tiklandi

[18:05]
Smena topshirildi
```

Shu ko'rinishda Excel va Word hujjatlariga ham tushadi — boshliq kun davomida ish qanday
ketganini vaqti bilan ko'radi. Muammolar va rejalar ham xuddi shunday to'planadi; bo'sh
qoldirilgan bo'lim tegilmaydi.

**«♻️ Butunlay almashtirish»** — xato yozilgan bo'lsa, kunlik hisobotni noldan yozadi.

## 👔 Boshqarma boshlig'i nima qiladi

| Tugma | Vazifasi |
|---|---|
| 📊 Bugungi hisobotlar | Bugun kelgan barcha hisobotlar + topshirmaganlar ro'yxati |
| ⏳ Topshirmaganlar | Hisobot yubormagan hodimlar (username bilan) |
| 📥 Excel (.xlsx) | Tanlangan davr hisobotlarini jadval ko'rinishida yuklab olish |
| 📥 Word (.docx) | O'sha ma'lumot rasmiy hujjat ko'rinishida, imzo joyi bilan |
| 👥 Hodimlar | Ro'yxat, oxirgi hisobotlari, **shaxsiy Excel/Word**, faollashtirish / o'chirish + botga ulanmaganlar |
| 📈 Statistika | Joriy oyda kim nechta hisobot topshirgani |

**Davr tanlash:** Bugun · Kecha · Shu hafta · Oxirgi 7 kun · Shu oy · Oxirgi 30 kun ·
yoki qo'lda: `01.08.2026 - 18.08.2026`

### 👤 Bitta hodimning shaxsiy hisoboti

«👥 Hodimlar» → hodimni tanlang → **«📥 Shaxsiy Excel»** yoki **«📥 Shaxsiy Word»** → davr.
Hujjatga faqat o'sha hodimning yozuvlari tushadi, sarlavha ostida esa uning ma'lumoti
ko'rsatiladi:

```
Hodim: FAMILIYA ISM SHARIF — Yetakchi muhandis (tabel №1234)
```

Fayl nomi ham alohida bo'ladi: `Hisobot_1234_2026-08-01_2026-08-18.xlsx`

## ⏰ Avtomatik xabarlar

- **08:00 · 12:00 · 16:00 · 20:00** — hisobot topshirmagan hodimlarga eslatma
  (hisobotini topshirganlar bezovta qilinmaydi)
- **23:59** — boshliqqa kunlik xulosa (kim topshirdi, kim yo'q)

Jadval `.env` orqali sozlanadi — boshlanish vaqti, oraliq va oxirgi eslatma chegarasi:

```
REMINDER_START=08:00
REMINDER_INTERVAL_HOURS=4
REMINDER_END=20:00
DIGEST_TIME=23:59
```
`WORKDAYS_ONLY=true` bo'lsa, eslatmalar faqat dushanba–juma kunlari yuboriladi.

---

## ☁️ Serverga joylashtirish (Render)

Bot polling rejimida ishlaydi, lekin Render ochiq port talab qiladi — shu sababli
[bot.py](bot.py) da kichik HTTP server bor (`/` → `Bot is running!`). `PORT` ni Render
o'zi beradi.

| Sozlama | Qiymat |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python bot.py` |

**Environment Variables** (`.env` GitHubda yo'q, shuning uchun qo'lda kiritiladi):
`BOT_TOKEN`, `ADMIN_IDS`, `ORG_NAME`, `CHIEF_NAME`, `CHIEF_NAME_RU`, `FOOTER_TEXT`,
`TIMEZONE`, `REMINDER_TIME`, `DIGEST_TIME`.

**Shtat ro'yxati:** `staff.json` ni Render'ning *Secret Files* bo'limiga yuklang va
`STAFF_FILE=/etc/secrets/staff.json` deb ko'rsating.

**Baza:** Render'da fayl tizimi har deploy'da tozalanadi. Hisobotlar saqlanib qolishi uchun
*Persistent Disk* ulang (masalan `/var/data`) va `DB_PATH=/var/data/reports.db` deb yozing.
Disksiz ishlatsangiz, har deploy'da hamma hisobot yo'qoladi.

## 📁 Fayllar tuzilishi

```
dailyreport_bot/
├── bot.py                  # ishga tushirish nuqtasi
├── config.py               # .env sozlamalari
├── staff.json              # SHTAT RO'YXATI (GitHubga tushmaydi)
├── staff.example.json      # uning namunasi
├── roster.py               # shtat ro'yxatini o'qish
├── i18n.py                 # BARCHA MATNLAR (o'zbekcha / ruscha)
├── database.py             # SQLite (hodimlar, hisobotlar, til sozlamasi)
├── keyboards.py            # tugmalar
├── filters.py              # tugma va admin filtrlari
├── middlewares.py          # foydalanuvchi tilini aniqlash
├── states.py               # suhbat bosqichlari (FSM)
├── flows.py                # umumiy oqim (hisobotni boshlash)
├── utils.py                # sana va matn yordamchilari
├── scheduler.py            # eslatma va kunlik xulosa
├── handlers/
│   ├── common.py           # til, /start, tabel orqali ro'yxatdan o'tish, /help
│   ├── employee.py         # hisobot topshirish
│   └── admin.py            # boshliq paneli, Excel/Word eksport
├── exporters/
│   ├── excel_export.py     # .xlsx shakllantirish
│   └── word_export.py      # .docx shakllantirish
├── data/reports.db         # ma'lumotlar bazasi (avtomatik yaratiladi)
├── requirements.txt
├── start.bat
└── .env                    # siz yaratasiz (.env.example dan)
```

## 💾 Ma'lumotlar

Hamma narsa `data/reports.db` faylida (SQLite). **Zaxira nusxa** olish uchun shu bitta
faylni nusxalab qo'yish kifoya. Bu faylni boshqa kompyuterga ko'chirsangiz, barcha
hisobotlar o'zi bilan ko'chadi.

## ❓ Tez-tez uchraydigan savollar

**Boshliq menyusi ko'rinmayapti.** `.env` dagi `ADMIN_IDS` ga to'g'ri raqam yozilganini
tekshiring va botni qayta ishga tushiring.

**Hodim ketdi / xato ro'yxatdan o'tdi.** «👥 Hodimlar» → hodimni tanlang →
«🚫 Faolsizlantirish» (hisobotlari saqlanib qoladi) yoki «🗑 O'chirish» (butunlay o'chadi).

**Bir nechta rahbar kerak.** `ADMIN_IDS=111111111,222222222` — vergul bilan ajrating.
Har biriga hamma xabar va fayl boradi.

**Rahbarning o'zi ham hisobot topshirsinmi?** U holda uning ID sini `ADMIN_IDS` ga
yozmang — yoki alohida (ikkinchi) Telegram akkaunti orqali hodim sifatida ro'yxatdan o'tsin.

**Bot doim ishlab turishi uchun.** Kompyuterni o'chirmang yoki botni serverga
(VPS/hosting) joylashtiring — o'sha yerda ham `python bot.py` kifoya.

