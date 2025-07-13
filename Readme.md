🧠 Smart PDF Research Assistant
Turn any PDF or TXT into an interactive study partner in < 2 minutes.
🚀 Live Demo
Open the Streamlit front-end after starting services:
http://localhost:8501
🏗️ Architecture & Reasoning Flow
Code
Preview
View Large Image
Download
Copy
graph TD
    A[User uploads PDF/TXT<br>(Streamlit)] -->|file bytes| B[FastAPI /upload]
    B --> C[doc_processor.py<br>- extracts text<br>- builds FAISS index]
    C --> D[Local FAISS Vector Store]
    D --> E[User asks question<br>(Streamlit)]
    E -->|QuestionRequest| F[FastAPI /ask]
    F --> G[llm_service.py<br>- similarity search<br>- Gemini context injection]
    G --> H[Answer + citations<br>returned to Streamlit]
    I[Challenge Me] -->|/challenges| G
    J[Evaluate Answer] -->|/evaluate| G
⚙️ Setup Instructions
1️⃣ Clone & enter repo
bash
Copy
git clone https://github.com/pushkar9897/smart-pdf-assist.git
cd smart-pdf-assist
2️⃣ Install dependencies
bash
Copy
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Configure secrets
bash
Copy
cp .env.example .env
# Edit .env
GOOGLE_GEMINI_API_KEY=your_key_here
4️⃣ Start services
Terminal 1 – Backend
bash
Copy
uvicorn backend.main:app --reload
Terminal 2 – Frontend
bash
Copy
streamlit run frontend/app.py
Open http://localhost:8501 and drag-&-drop your first PDF!
📁 Source Code Layout
Copy
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
🎯 Optional Demo Walkthrough
2-min Loom video: (link will be inserted after recording)
Covering: upload ➜ ask ➜ challenge ➜ evaluate.
📝 Environment Variables
Table
Copy
Variable	Purpose
GOOGLE_GEMINI_API_KEY	Google Generative AI key (required)
🔧 Performance Tips
Install watchdog for faster hot-reload:
bash
Copy
pip install watchdog
Very large PDFs (~100 MB) may take ~30 s on first indexing—be patient.
Happy learning!
