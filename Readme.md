# 🧠 SMART PDF RESEARCH ASSISTANT

Turn any **PDF or TXT into an interactive study partner** in under 2 minutes.

---

## 🚀 LIVE DEMO

👉 Open the **Streamlit front-end** after starting services:  
**[http://localhost:8501](http://localhost:8501)**

---

## 🏗️ ARCHITECTURE & REASONING FLOW

graph TD
    A[User uploads PDF/TXT (Streamlit)] -->|file bytes| B[FastAPI /upload]
    B --> C[doc_processor.py - extracts text - builds FAISS index]
    C --> D[Local FAISS Vector Store]
    D --> E[User asks question (Streamlit)]
    E -->|QuestionRequest| F[FastAPI /ask]
    F --> G[llm_service.py - similarity search - Gemini context injection]
    G --> H[Answer + citations returned to Streamlit]
    I[Challenge Me] -->|/challenges| G
    J[Evaluate Answer] -->|/evaluate| G
---

## ⚙️ SETUP INSTRUCTIONS

### 1️⃣ CLONE & ENTER REPO
```bash
git clone https://github.com/pushkar9897/smart-pdf-assist.git
cd smart-pdf-assist
```

### 2️⃣ INSTALL DEPENDENCIES
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ CONFIGURE SECRETS
```bash
cp .env.example .env
# Edit .env and add:
GOOGLE_GEMINI_API_KEY=your_key_here
```

### 4️⃣ START SERVICES

**Terminal 1 – Backend**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 – Frontend**
```bash
streamlit run frontend/app.py
```

🔗 Open **http://localhost:8501** and drag-&-drop your first PDF!

---

## 📁 SOURCE CODE LAYOUT

```
smart-pdf-assist/
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── api_models.py     # Pydantic schemas
│   ├── doc_processor.py  # PDF/TXT → text → FAISS index
│   ├── llm_service.py    # Gemini chat & quiz logic
│   └── config.py         # env loader
├── frontend/
│   └── app.py            # Streamlit UI
├── .env.example          # template
├── requirements.txt
└── README.md
```

---

YOUTUBE VEDIO LINK :

📽️ **2-min Loom video:** _(link will be inserted after recording)_  
_Covering:_ upload ➜ ask ➜ challenge ➜ evaluate

---

## 📝 ENVIRONMENT VARIABLES

| Variable               | Purpose                                    |
|------------------------|--------------------------------------------|
| `GOOGLE_GEMINI_API_KEY` | Google Generative AI key (**required**)   |

---

## 🔧 PERFORMANCE TIPS

- Install `watchdog` for faster hot-reload:
  ```bash
  pip install watchdog
  ```

- Very large PDFs (~100 MB) may take ~30 sec on first indexing — **be patient**.

---

🎉 **Happy learning!**

