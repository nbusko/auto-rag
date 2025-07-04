import logging
from fastapi import APIRouter, HTTPException
from datetime import datetime
from config.contracts import RAGRequest, RAGResponse
from rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)
router = APIRouter()
rag_pipeline = RAGPipeline()

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

        logger.info(f"Processing user message: {request.user_message[:100]}...")

        result = await rag_pipeline.process_rag_request(
            request.chat_id,
            request.user_message,
            str(request.document_id),
            request.message_id,
            request.llm,
            request.prompt_retrieve,
            request.prompt_augmentation,
            request.prompt_generation,
            request.top_k,
            request.temperature,
            request.threshold,
            request.embeddings,
            request.text_chunks,
        )

        if result.status == "error":
            logger.error(f"RAG processing failed : {result.message}")
            return result

        logger.info(
            f"RAG request processed for chat_id: {request.chat_id} with result: {result.generated_answer}"
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error processing RAG request: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Error processing RAG request: {str(e)}"
        )
