✨ Smart PDF Research Assistant ✨
Turn any PDF or TXT into an interactive study partner.
🚀 Live Demo
Try the app instantly:
http://localhost:8501
🌟 What it does

Upload 📄	                                             	        
Drag-&-drop a PDF or TXT.	
-------------------------------------------------------------------------------------------------------
Ask 🤔
Ask anything—get citations + answers. 
-------------------------------------------------------------------------------------------------------

Challenge 🎯
AI crafts unique quiz questions.
-------------------------------------------------------------------------------------------------------
Evaluate ✅
Submit answers, get instant feedback.
-------------------------------------------------------------------------------------------------------

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| **Backend** | FastAPI • LangChain • FAISS • Google Gemini |
| **Frontend** | Streamlit |
| **Embeddings** | `all-MiniLM-L6-v2` |
| **Vector DB** | FAISS (local, lightning-fast) |

## 🚀 Quick Start

### 1️⃣ Clone & enter repo
```bash
git clone https://github.com/pushkar9897/smart-pdf-assist.git
cd smart-pdf-assist

2️⃣ Install deps
        pip install -r requirements.txt
3️⃣ Add your API key
        cp .env.example .env
        # Edit .env
        GOOGLE_GEMINI_API_KEY=your_key_here
4️⃣ Fire it up
Terminal 1 – Backend
            uvicorn backend.main:app --reload
Terminal 2 – Frontend
            streamlit run frontend/app.py
🎉 Open localhost:8501 and start learning smarter!
📁 Project Layout

smart-pdf-assist/
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── api_models.py     # Pydantic schemas
│   ├── doc_processor.py  # PDF / TXT indexing
│   ├── llm_service.py    # Gemini chat & quiz logic
│   └── config.py         # env loader
├── frontend/
│   └── app.py            # Streamlit UI
├── .env.example          # template
├── requirements.txt
└── README.md
⚙️ Environment Variables
|Variable               |	 Purpose
|GOOGLE_GEMINI_API_KEY	|  Your Google Gemini API key (required)
📈 Performance Tips
Install watchdog for faster reloads:

        pip install watchdog
Large PDFs? First upload may take ~30 s for indexing—be patient!

