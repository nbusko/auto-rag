import logging
import os
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, HTTPException

from datetime import datetime
import os
from config.contracts import RAGRequest, RAGResponse

from main import rag_pipeline


logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "RAG Service is running", "docs": "/docs"}

@router.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "timestamp": datetime.now()}

@router.post("/rag/process", response_model=RAGResponse)
async def process_rag_request(request: RAGRequest):
    """Обработать RAG запрос"""
    logger.info(f"Processing RAG request for chat_id: {request.chat_id}")
    try:
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OpenAI API key not configured")
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key not configured"
            )
        
        logger.info(f"Processing user message: {request.user_message[:100]}...")
        
        # Обрабатываем RAG запрос
        result = rag_pipeline.process_rag_request(
            **request.model_dump()
        )
        
        # Проверяем на ошибки
        if "error" in result:
            logger.error(f"RAG processing error: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"RAG request processed successfully for chat_id: {request.chat_id}")
        
        return RAGResponse(
            chat_id=result["chat_id"],
            message_id=result["message_id"],
            assistant_message=result["assistant_message"],
            retrieved_chunks=result["retrieved_chunks"],
            similarity_scores=result["similarity_scores"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing RAG request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing RAG request: {str(e)}")
