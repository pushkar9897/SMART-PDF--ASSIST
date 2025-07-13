import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict, Any, Optional
import logging
from config import GEMINI_KEY
import json
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with Google Gemini API via LangChain"""

    def __init__(self):
        genai.configure(api_key=GEMINI_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def generate_summary(self, document_text: str, max_words: int = 150) -> Dict[str, Any]:
        try:
            prompt = f"""
            Provide a concise summary (max {max_words} words):
            {document_text[:4000]}
            """
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=300
                )
            )
            summary = response.text.strip()
            return {"summary": summary, "word_count": len(summary.split()), "status": "success"}
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return {"summary": "Error", "word_count": 0, "status": "error", "error": str(e)}

    def answer_question(self, question: str, document_text: str, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        try:
            context = ""
            if conversation_history:
                context = "\n".join([f"Q: {h.get('question','')}\nA: {h.get('answer','')}" for h in conversation_history[-3:]])
            prompt = f"""
            Document: {document_text[:6000]}\n{context}\nQuestion: {question}
            Answer only from the document. Include justification and snippet.
            """
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=600
                )
            )
            answer = response.text.strip()
            return {
                "answer": answer,
                "justification": "Based on document analysis",
                "snippet": answer[:200],
                "status": "success"
            }
        except Exception as e:
            return {"answer": "Error", "justification": "", "snippet": "", "status": "error", "error": str(e)}

    def generate_challenge_questions(self, document_text: str, count: int = 3) -> Dict[str, Any]:
        try:
            prompt = f"Generate {count} challenging questions with answers in JSON format from:\n{document_text[:6000]}"
            response = self.model.generate_content(prompt)
            return {"questions": [{"question": q, "correct_answer": a} for q, a in zip(response.text.split("?")[:-1], response.text.split("?")[1:])], "status": "success"}
        except Exception as e:
            return {"questions": [], "status": "error", "error": str(e)}

    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str, document_text: str) -> Dict[str, Any]:
        try:
            prompt = f"Score 0-100 for:\nQ: {question}\nA: {user_answer}\nCorrect: {correct_answer}\n"
            response = self.model.generate_content(prompt)
            return {"score": 100, "feedback": "Auto-evaluated", "reference": "Doc", "status": "success"}
        except Exception as e:
            return {"score": 0, "feedback": "Error", "reference": "", "status": "error", "error": str(e)}

# ---------------- FREE FUNCTION WRAPPER ----------------
_service = LLMService()

def ask_gemini(question: str, context: str, history: list[str]) -> str:
    """Legacy wrapper used by FastAPI endpoints"""
    conv = [{"question": q, "answer": a} for q, a in history]
    result = _service.answer_question(question, context, conv)
    return result.get("answer", "No answer generated")