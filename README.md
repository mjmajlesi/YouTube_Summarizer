<div align="center">

# 🎬 YouTube Summarizer

### خلاصه هوشمند ویدیوهای یوتیوب — از TF-IDF تا Transformer

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/mjmajlesi/YouTube_Summarizer/pulls)

**لینک یوتیوب بده، خلاصه تحویل بگیر — فارسی و انگلیسی، با ترجمه یک‌کلیکه.**

[ویژگی‌ها](#-ویژگیها) • [دمو](#-دمو) • [شروع سریع](#-شروع-سریع) • [معماری](#-معماری) • [API](#-api) • [نقشه راه](#-نقشه-راه) • [مشارکت](#-مشارکت)

</div>

---

## ✨ ویژگی‌ها

| قابلیت | وضعیت |
|---|---|
| 🎥 استخراج Transcript از هر ویدیو یوتیوب (حتی `fa` auto-generated) | ✅ فاز 0 |
| 📝 خلاصه Extractive با TF-IDF / TextRank | 🔜 فاز 1 |
| 🤖 خلاصه Abstractive با BART / mT5 / Pegasus | 🔜 فاز 2 |
| 🌐 ترجمه خلاصه (en ↔ fa) با یک کلیک | 🔜 فاز 2.5 |
| 🕘 تاریخچه + کش + چپتربندی | 🔜 فاز 3–4 |
| 🐳 داکر + دیپلوی Vercel/Railway | 🔜 فاز 5 |

---

## 🎥 دمو

> بعد از دیپلوی، GIF اینجا قرار می‌گیرد.

```
YouTube URL → [ خلاصه کن ] → خلاصه فارسی/انگلیسی → [ 🌐 ترجمه به فارسی ]
```

---

## 🧱 معماری

```
┌─────────────┐      POST /summarize       ┌──────────────────┐
│  Next.js 16 │  ──────────────────────►   │  FastAPI         │
│  (App Router│                            │  ├─ extract_id   │
│   + Tailwind)│  ◄──────────────────────   │  ├─ transcript   │
└─────────────┘      { summary }           │  ├─ TF-IDF (ph1) │
                                           │  ├─ BART/mT5(ph2)│
                                           │  └─ translate   │
                                           └──────────────────┘
                                                    │
                                          youtube_transcript_api
                                           transformers / torch
```

**ساختار پروژه:**

```
YouTube_Summarizer/
├── backend/
│   ├── main.py          # FastAPI app + CORS + /summarize
│   ├── transcript.py    # extract_video_id + getTranscript + summary
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # فرم + fetch + نمایش خلاصه
│   │   ├── layout.tsx
│   │   ├── globals.css       # Tailwind v4
│   │   └── components/Head.tsx
│   ├── package.json
│   └── next.config.ts
├── ROADMAP.md           # نقشه راه کامل فاز 1 تا 5 (فارسی)
└── README.md
```

---

## 🚀 شروع سریع

### پیش‌نیازها

- Python 3.11+
- Node.js 18+
- یک ویدیو یوتیوب با زیرنویس (یا auto-generated)

### 1) بک‌اند

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# → http://localhost:8000/docs  (Swagger)
```

### 2) فرانت‌اند

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 3) متغیر محیطی (اختیاری)

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

حالا یک URL مثل `https://www.youtube.com/watch?v=DpbDoRjuWfk` را در فرانت وارد کن.

---

## 🔌 API

### `GET /`

```json
{ "message": "Backend is running" }
```

### `POST /summarize`

```json
// Request
{ "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" }

// Response 200
{ "summary": "خلاصه 5 جمله‌ای ..." }

// Errors
400 → { "detail": "Invalid YouTube URL" }
404 → { "detail": "No transcripts available for this video" }
```

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

> در فاز 1 به بعد: `POST /summarize?method=tfidf|abstractive` و `POST /translate` اضافه می‌شود.

---

## 🗺️ نقشه راه

تمام جزئیات فاز 1 تا 5 با تسک‌های چک‌لیستی، منابع یادگیری و ترتیب پیشنهادی در فایل زیر است:

📄 **[ROADMAP.md](ROADMAP.md)** — به زبان فارسی، مرحله‌به‌مرحله، مخصوصاً فاز 2 (Deep Learning) با دو مسیر محصول/آموزشی + بخش ترجمه.

**ترتیب پیشنهادی:**

```
فاز 1 (TF-IDF، 2 روز) → فاز 2A (BART آماده، 1 روز) → فاز 2.5 (ترجمه، 1 روز)
       → فاز 3 (فرانت، 3 روز) → فاز 2B (فاین‌تیون، موازی) → فاز 4 → فاز 5
```

---

## 🌐 ترجمه خلاصه (فاز 2.5 — به‌زودی)

ایده: کاربر خلاصه انگلیسی را با یک دکمه به فارسی ترجمه کند (و برعکس) — بدون نیاز به API پولی:

- مدل لوکال: `Helsinki-NLP/opus-mt-en-fa` (~300MB، رایگان)
- یا `facebook/nllb-200-distilled-600M` (کیفیت بالاتر)
- کش ترجمه + تشخیص خودکار زبان مبدأ

جزئیات کامل در `ROADMAP.md` بخش 2.5.

---

## 🛠️ تکنولوژی‌ها

| لایه | تکنولوژی |
|---|---|
| Frontend | Next.js 16 (App Router), React 19, Tailwind v4, TypeScript |
| Backend | FastAPI, Pydantic, youtube-transcript-api |
| NLP (فعلی) | TF-IDF (scikit-learn) — به‌زودی |
| Deep Learning | transformers, PyTorch, BART/mT5/Pegasus, ROUGE |
| Translate | MarianMT (Helsinki-NLP), NLLB |
| Infra (آینده) | Docker, Vercel, Railway/Render, GitHub Actions |

---

## 🤝 مشارکت

PRها آزادند! لطفاً هر فاز را در یک برنچ جدا (`feat/phase-1-tfidf`, `feat/phase-2-abstractive`, ...) بزنید.

```bash
git checkout -b feat/phase-1-tfidf
# ... تغییرات ...
git commit -m "feat: tfidf summarizer"
gh pr create
```

---

## 📄 لایسنس

[MIT](LICENSE) — آزاد برای استفاده شخصی و تجاری.

---

<div align="center">

**ساخته شده با ☕ و 🎧 — اگر به دردت خورد ⭐ بده!**

</div>
