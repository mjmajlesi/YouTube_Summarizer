# 🗺️ YouTube Summarizer — نقشه راه کامل (فاز 1 تا 5)

> این فایل رودمپ تکمیل پروژه است. فاز 0 قبلاً مرج شد. از اینجا به بعد هر فاز یک PR جداست.

---

## فاز 1 — خلاصه‌سازی Extractive با TF-IDF (2 تا 3 روز)

> هدف: بدون Deep Learning، فقط با NLP کلاسیک یک خلاصه واقعی بسازی. پیش‌نیاز ذهنی عالی برای فاز 2.

### 1.1 چی باید بسازی؟
الان `summary()` فقط 5 جمله اول رو برمیگردونه. باید با TF-IDF مهم‌ترین جملات را انتخاب کنی.

### 1.2 تسک‌ها
- [ ] `pip install scikit-learn nltk`
- [ ] `transcript.py` → تابع `summary_tfidf(text, k=5)`:
  1. متن را به جملات بشکن (`nltk.sent_tokenize` یا `re.split(r'[.!?]+')`)
  2. هر جمله = یک document برای `TfidfVectorizer(stop_words='english')`
  3. امتیاز هر جمله = میانگین TF-IDF وزن کلماتش (یا جمع — هر دو را تست کن)
  4. top-k جمله را به ترتیب اصلی متن برگردان (نه ترتیب امتیاز — خوانایی مهمه)
- [ ] فارسی را هم ساپورت کن: برای `fa` از `stop_words` دستی یا `hazm` استفاده کن
- [ ] یک baseline دوم با TextRank بساز (`networkx` + cosine similarity بین جملات) تا مقایسه کنی کدوم بهتره
- [ ] یک اسکریپت ارزیابی ساده: روی 10 ویدیو، خروجی TF-IDF vs اول-5-جمله را کنار هم لاگ بگیر و چشمی مقایسه کن

### 1.3 مفاهیم برای یادگیری
| مفهوم | چرا |
|---|---|
| Bag of Words / TF-IDF | وزن‌دهی کلمات |
| Cosine Similarity | شباهت جملات |
| Stopwords / Stemming | نویزگیری |

### 1.4 خروجی فاز
- `POST /summarize?method=tfidf` کار میکند
- تست دستی روی 3 ویدیو فارسی + 3 انگلیسی

### 1.5 منابع
- [scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [TextRank paper](https://arxiv.org/abs/1602.03438)

---

## فاز 2 — خلاصه‌سازی Abstractive با Deep Learning ⭐️ (1 تا 2 هفته) — فاز اصلی تو

> این فاز قلب پروژه و بخش یادگیری Deep Learning توست. دو مسیر داری — هر دو را بخوان، یکی را برای محصول و یکی را برای یادگیری برو.

### 2.0 پیش‌نیازهای تئوری (قبل از کد — 3 تا 4 روز مطالعه)

| مبحث | عمق مورد نیاز | منبع پیشنهادی |
|---|---|---|
| Perceptron / MLP / Backprop | بفهمی گرادیان چطور برمیگرده | 3Blue1Brown – Neural Networks (یوتیوب) |
| RNN / LSTM / GRU | چرا برای متن طولانی می‌شکنه | colah.github.io – Understanding LSTM |
| Attention / Self-Attention | فرمول `softmax(QKᵀ/√d)V` را دستی حساب کنی | Jay Alammar – The Illustrated Transformer |
| Transformer (Encoder-Decoder) | معماری کامل + Positional Encoding | Attention Is All You Need (paper) + Hugging Face course ch.1 |
| Seq2Seq + Beam Search | چطور خلاصه تولید میشود | Hugging Face – Summarization chapter |
| Transfer Learning / Fine-tuning | چرا از صفر آموزش نمیدهیم | HF – Fine-tuning a model |

> اگر فقط یک کار بکنی: **Hugging Face NLP Course (ch 1, 7)** را کامل برو — رایگان و عملیه.

### 2.1 مسیر A — محصول (سریع، 1 تا 2 روز)

> با مدل آماده، بدون آموزش، فقط inference.

- [ ] `pip install transformers torch --index-url https://download.pytorch.org/whl/cpu` (یا `+cu121` اگر GPU داری)
- [ ] یک تابع `summary_abstractive(text, max_length=150)`:
  ```python
  from transformers import pipeline
  summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
  # یا برای فارسی: "facebook/mbart-large-50" یا "google/mt5-small"
  ```
- [ ] **چانک کردن**: مدل‌ها max 1024 توکن میگیرند، ویدیو 10 دقیقه‌ای ~2000 توکنه
  - متن را به چانک‌های 800 توکن بشکن (با overlap 100)
  - هر چانک را خلاصه کن، بعد خلاصه‌ها را دوباره خلاصه کن (map-reduce)
- [ ] بک‌اند: `POST /summarize?method=abstractive` را اضافه کن (فاز 1 را نشکن)
- [ ] کش مدل: بار اول دانلود ~1.5GB طول میکشه — با `TRANSFORMERS_CACHE` مدیریت کن

**مدل‌های پیشنهادی به ترتیب:**
1. `facebook/bart-large-cnn` — بهترین برای انگلیسی
2. `google/pegasus-xsum` — خلاصه‌های کوتاه‌تر و انتزاعی‌تر
3. `facebook/mbart-large-50` — چندزبانه (انگلیسی↔فارسی)
4. `google/mt5-small` — سبک، برای فاین‌تیون بعدی

### 2.2 مسیر B — آموزشی / فاین‌تیون (عمیق، 1 هفته)

> اینجا واقعاً Deep Learning یاد میگیری. این مسیر را در یک برنچ جدا (`ml/finetune-mt5`) برو.

#### گام B1 — دیتاست
- [ ] دیتاست `cnn_dailymail` (انگلیسی) یا `wiki_lingua` (فارسی) را از Hugging Face Datasets بگیر:
  ```python
  from datasets import load_dataset
  ds = load_dataset("cnn_dailymail", "3.0.0")
  # یا برای فارسی:
  ds = load_dataset("wiki_lingua", "english_persian")
  ```
- [ ] 1000 نمونه را برای تست سریع جدا کن (full dataset = 300k، سنگینه)

#### گام B2 — توکنایزر و Data Collator
- [ ] `AutoTokenizer.from_pretrained("google/mt5-small")`
- [ ] `max_input_length=512`, `max_target_length=128`
- [ ] `DataCollatorForSeq2Seq` برای padding دینامیک

#### گام B3 — آموزش
- [ ] `Seq2SeqTrainer` یا `Trainer` از `transformers` + `TrainingArguments`
- [ ] هایپرپارام شروع: `lr=5e-5`, `batch=4`, `epochs=3`, `warmup_steps=500`
- [ ] اگر GPU نداری: از **Kaggle (30h free GPU)** یا **Colab T4** استفاده کن
- [ ] لاگ با `wandb` یا `tensorboard`

#### گام B4 — ارزیابی
- [ ] متریک اصلی: **ROUGE** (`rouge1`, `rouge2`, `rougeL`) — با `evaluate` یا `rouge-score`
  ```python
  import evaluate
  rouge = evaluate.load("rouge")
  rouge.compute(predictions=preds, references=refs)
  ```
- [ ] متریک تکمیلی: `BERTScore` (معنایی‌تر از ROUGE)
- [ ] یک baseline مقایسه: TF-IDF (فاز 1) vs BART zero-shot vs مدل فاین‌تیون‌شده — جدول ROUGE بساز

#### گام B5 — خروجی
- [ ] مدل فاین‌تیون‌شده را روی Hugging Face Hub پوش کن (`push_to_hub=True`)
- [ ] یک `notebooks/eval.ipynb` با نمودار ROUGE و نمونه خلاصه‌ها

### 2.3 چک‌لیست یادگیری فاز 2
- [ ] میتونی با چشم بسته معماری Transformer را روی کاغذ بکشی
- [ ] فهمیدی چرا Beam Search بهتر از Greedy است
- [ ] یک بار loss curve را دیدی و فهمیدی overfitting کجاست
- [ ] ROUGE را دستی برای یک مثال حساب کردی

### 2.4 منابع گلچین
- 📘 [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course/chapter1/1) — واجب
- 📄 [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- 📄 [BART paper](https://arxiv.org/abs/1910.13461)
- 📄 [mT5 paper](https://arxiv.org/abs/2010.11934)
- 🎥 [Yannic Kilcher – BART explained](https://youtu.be/iOyjaJkG7yM)

---

## فاز 2.5 — ترجمه خلاصه به فارسی 🌐 (جدید — ایده تو)

> کاربر خلاصه انگلیسی را با یک کلیک به فارسی ترجمه کند (و برعکس).

### 2.5.1 گزینه‌های پیاده‌سازی

| گزینه | مزیت | هزینه |
|---|---|---|
| **A. مدل لوکال `Helsinki-NLP/opus-mt-en-fa`** | رایگان، آفلاین، حریم خصوصی | ~300MB، کیفیت متوسط |
| **B. `facebook/nllb-200-distilled-600M`** | کیفیت عالی، 200 زبان | ~2GB، کندتر |
| **C. Google Translate API** | کیفیت عالی، سریع | پولی، نیاز به API key |
| **D. `google/mt5` / `mbart-50` چندزبانه** | یک مدل برای خلاصه+ترجمه | پیچیده‌تر |

> پیشنهاد: با **A** شروع کن (رایگان و سریع)، اگر کیفیت کم بود برو **B**.

### 2.5.2 تسک‌ها
- [ ] `pip install transformers sentencepiece sacremoses` (برای opus-mt)
- [ ] بک‌اند: `POST /translate` → `{ text, target_lang: "fa" | "en" }`
  ```python
  from transformers import MarianMTModel, MarianTokenizer
  model_name = "Helsinki-NLP/opus-mt-en-fa"  # یا fa-en
  tokenizer = MarianTokenizer.from_pretrained(model_name)
  model = MarianMTModel.from_pretrained(model_name)
  ```
- [ ] فرانت: زیر هر خلاصه یک دکمه `🌐 ترجمه به فارسی` — نتیجه را زیر خلاصه اصلی نشان بده (هر دو را نگه دار)
- [ ] کش ترجمه: `(hash(text), lang)` را در `dict` یا `sqlite` کش کن تا دوباره ترجمه نکنی
- [ ] اگر خواستی حرفه‌ای شی: زبان مبدأ را auto-detect کن (`langdetect` یا `fasttext`)

### 2.5.3 نکته
- ترجمه بعد از خلاصه ارزان‌تر از ترجمه کل ترانسکریپت است (کمتر توکن)
- برای ویدیوهای فارسی که خلاصه فارسی دارند، دکمه را برعکس کن: `Translate to English`

---

## فاز 3 — تکمیل فرانت‌اند (3 تا 4 روز)

- [ ] نمایش خلاصه + دکمه کپی + شمارش کلمات/کاراکتر
- [ ] انتخاب متد: `TF-IDF | Abstractive | Translate` با `Tabs` یا `Select`
- [ ] نمایش Transcript اصلی با timestamp قابل کلیک (اگر API تایم‌استمپ بده — الان نمیده، باید `transcript.py` را ارتقا بدی تا `start/duration` را هم برگردونه)
- [ ] چپتربندی: اگر ویدیو chapter داره، خلاصه per-chapter
- [ ] تاریخچه: `localStorage` برای ذخیره 20 خلاصه آخر + دکمه حذف
- [ ] حالت دارک/لایت + ریسپانسیو موبایل
- [ ] اسکلتون لودینگ و Empty State زیبا

---

## فاز 4 — فیچرهای محصول (1 هفته)

- [ ] **کش**: `functools.lru_cache` یا `sqlite` برای `(video_id, method)` — همون ویدیو دوباره API نخوره
- [ ] **Rate Limit**: `slowapi` برای جلوگیری از اسپم
- [ ] **اعتبارسنجی**: URL واقعاً یوتیوب باشد، ویدیو private نباشد
- [ ] **Fallback بدون زیرنویس**: اگر transcript نبود → دانلود صدا با `yt-dlp` + `openai-whisper` (لوکال) — این خودش یک مینی‌پروژه‌ست
- [ ] **خلاصه بلند/کوتاه**: پارامتر `length: short | medium | long` → `max_length` مدل را تغییر بده
- [ ] **Auth (اختیاری)**: اگر خواستی تاریخچه را سروری نگه داری → `JWT` + `SQLite/Postgres`

---

## فاز 5 — دیپلوی و پولیش (2 تا 3 روز)

- [ ] `Dockerfile` برای `backend` + `frontend` + `docker-compose.yml`
- [ ] فرانت روی **Vercel** (رایگان، Next.js native)
- [ ] بک روی **Railway / Render / Fly.io** (یکی را انتخاب کن — همه tier رایگان دارند)
- [ ] `CORS` را از `allow_origins=["*"]` به دامنه واقعی تغییر بده
- [ ] `README` + اسکرین‌شات + دمو GIF
- [ ] CI ساده: `GitHub Actions` → `pytest` + `eslint` روی هر PR

---

## ترتیب پیشنهادی اجرا

```
فاز 1 (TF-IDF) → فاز 2A (BART آماده) → فاز 2.5 (ترجمه) → فاز 3 (فرانت) → فاز 2B (فاین‌تیون آموزشی) → فاز 4 → فاز 5
         ↑                ↑                    ↑
      2 روز            1 روز               1 روز
```

> فاز 2B را موازی با فاز 3/4 جلو ببر — چون نیاز به GPU و زمان آموزش دارد و بلاک‌کننده نیست.

---

## چطور از این فایل استفاده کنی؟

1. هر فاز را یک برنچ جدا بزن: `feat/phase-1-tfidf`, `feat/phase-2-abstractive`, ...
2. هر چک‌باکس که تمام شد تیک بزن و کامیت کن
3. اگر سوالی داشتی، شماره فاز را بگو تا عمیق‌تر بریم
