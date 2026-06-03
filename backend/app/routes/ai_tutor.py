from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AIChat
from app.schemas import AIQuestionRequest, AIAnswerResponse, AIChatHistoryResponse
import httpx
from app.config import settings

router = APIRouter(prefix="/api/v1/ai", tags=["ai-tutor"])

async def get_ollama_response(question: str) -> str:
    """
    Get response from Ollama LLM
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OLLAMA_API_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": question,
                    "stream": False
                },
                timeout=60.0
            )
            data = response.json()
            return data.get("response", "Unable to generate response")
    except Exception as e:
        return f"Error: {str(e)}"

@router.post("/ask", response_model=AIAnswerResponse)
async def ask_ai(
    question_data: AIQuestionRequest,
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Ask AI Tutor a question
    """
    # Get response from Ollama
    answer = await get_ollama_response(question_data.question)
    
    # Save to database
    chat = AIChat(
        user_id=user_id,
        question=question_data.question,
        answer=answer,
        question_type=question_data.question_type,
        answer_type="text"
    )
    
    db.add(chat)
    db.commit()
    db.refresh(chat)
    
    return AIAnswerResponse(
        id=chat.id,
        question=chat.question,
        answer=chat.answer,
        answer_type=chat.answer_type,
        created_at=chat.created_at
    )

@router.get("/history/{user_id}", response_model=AIChatHistoryResponse)
async def get_chat_history(user_id: str, db: Session = Depends(get_db), limit: int = 50):
    """
    Get AI chat history for user
    """
    chats = db.query(AIChat).filter(AIChat.user_id == user_id).order_by(AIChat.created_at.desc()).limit(limit).all()
    
    return AIChatHistoryResponse(
        chats=chats,
        total=len(chats)
    )

@router.delete("/history/{user_id}")
async def clear_history(user_id: str, db: Session = Depends(get_db)):
    """
    Clear AI chat history for user
    """
    db.query(AIChat).filter(AIChat.user_id == user_id).delete()
    db.commit()
    
    return {"message": "Chat history cleared"}
