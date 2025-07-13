from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime
import uuid
from typing import Dict, Any
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

from api_models import (
    DocumentUploadResponse, QuestionRequest, QuestionResponse, ChallengeQuestion,
    ChallengeQuestionsRequest, EvaluateAnswerRequest
)
from doc_processor import save_doc_and_index, summarize, build_vector_index, load_text
from llm_service import ask_gemini
from config import GEMINI_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Research Assistant API",
    description="AI-powered document analysis and question answering system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data")
index_cache = {}
documents_storage: Dict[str, Dict[str, Any]] = {}

@app.get("/health", response_model=dict)
async def health_check():
    return {"status": "ok"}

def get_index(doc_id):
    if doc_id in index_cache:
        return index_cache[doc_id]
    idx_path = DATA_DIR / f"{doc_id}.faiss"
    if not idx_path.exists():
        raise HTTPException(404, "Index not found for document")
    index = FAISS.load_local(idx_path, SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)
    index_cache[doc_id] = index
    return index

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        doc_id, text = save_doc_and_index(file_bytes, file.filename)
        summary = summarize(text)
        documents_storage[doc_id] = {
            "doc_id": doc_id,
            "filename": file.filename,
            "text": text,
            "summary": summary,
            "upload_timestamp": datetime.now(),
            "status": "ready"
        }
        logger.info(f"Document uploaded: {doc_id}")
        return DocumentUploadResponse(
            status="success",
            message="Document uploaded successfully",
            document_id=doc_id,  # <-- use document_id
            filename=file.filename,
            word_count=len(text.split()),
            char_count=len(text),
            file_type=Path(file.filename).suffix,
            summary=summary
        )
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(req: QuestionRequest):
    try:
        if req.document_id not in documents_storage:
            raise HTTPException(404, "Document not found")
        document = documents_storage[req.document_id]
        index = get_index(req.document_id)
        docs = index.similarity_search(req.question, k=5)
        context = "\n".join([d.page_content for d in docs])
        context = context[:2000]
        logging.warning("Calling Gemini API...")
        answer = ask_gemini(req.question, context, req.conversation_history)
        logging.warning("Gemini API returned.")
        return QuestionResponse(
            answer=answer,
            justification="Generated from retrieved context.",
            snippet=context[:400] + "...",
            status="success" 
        )
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/challenges", response_model=list[ChallengeQuestion])
async def generate_challenge_questions(document_id: str, count: int = 3):
    try:
        if document_id not in documents_storage:
            raise HTTPException(404, "Document not found")
        index = get_index(document_id)
        docs = index.similarity_search("key points", k=count)
        challenges = []
        for i, d in enumerate(docs):
            prompt = (
                f"Given the document chunk below, create **one** challenging question that can **only** be answered "
                f"from this excerpt. Provide your answer in exactly three lines:\n"
                f"Q: <your question>\n"
                f"A: <one-line correct answer>\n"
                f"Justification: <brief explanation>\n\n"
                f"{d.page_content}"
            )
            result = ask_gemini(prompt, context="", history=[])
            lines = [ln.strip() for ln in result.strip().splitlines() if ln.strip()]
            q = next((ln[3:].strip() for ln in lines if ln.startswith("Q:")), f"Unparsed question for chunk {i+1}")
            a = next((ln[3:].strip() for ln in lines if ln.startswith("A:")), d.page_content.split(".")[0])
            j = next((ln[14:].strip() for ln in lines if ln.startswith("Justification:")), d.page_content[:200])
            challenges.append(ChallengeQuestion(question=q, correct_answer=a, explanation=j, difficulty="medium")
            )
        return challenges
    except Exception as e:
        logger.error(f"Error generating challenge questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate", response_model=dict)
async def evaluate_answer(req: EvaluateAnswerRequest):
    try:
        index = get_index(req.document_id)
        docs = index.similarity_search("key points", k=3)
        gold = docs[req.challenge_index].page_content.split(".")[0]
        correct = req.user_answer.strip().lower() in gold.lower()
        return {"correct": correct, "explanation": docs[req.challenge_index].page_content[:200]}
    except Exception as e:
        logger.error(f"Error evaluating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document/{doc_id}", response_model=dict)
async def get_document_info(doc_id: str):
    try:
        if doc_id not in documents_storage:
            raise HTTPException(404, "Document not found")
        doc = documents_storage[doc_id]
        return {
            "doc_id": doc_id,
            "filename": doc["filename"],
            "summary": doc["summary"],
            "upload_timestamp": doc["upload_timestamp"]
        }
    except Exception as e:
        logger.error(f"Error getting document info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/document/{doc_id}", response_model=dict)
async def delete_document(doc_id: str):
    try:
        if doc_id not in documents_storage:
            raise HTTPException(404, "Document not found")
        del documents_storage[doc_id]
        logger.info(f"Document deleted: {doc_id}")
        return {"status": "success", "message": "Document deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred", "error_code": "INTERNAL_ERROR"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )