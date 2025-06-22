import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from datetime import datetime
import os

from models import RAGRequest, RAGResponse
from database import DatabaseManager
from rag_pipeline import RAGPipeline

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('rag_service.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Service", 
    version="1.0.0",
    description="Сервис для обработки RAG запросов и генерации ответов на основе контекста",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализируем сервисы
logger.info("Initializing RAG Service...")
db_manager = DatabaseManager()
rag_pipeline = RAGPipeline()
logger.info("RAG Service initialized successfully")

@app.on_event("startup")
async def startup_event():
    logger.info("RAG Service starting up...")
    try:
        # Проверяем подключение к базе данных
        await db_manager.test_connection()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("RAG Service shutting down...")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "RAG Service is running", "docs": "/docs"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/rag/process", response_model=RAGResponse)
async def process_rag_request(request: RAGRequest):
    """Обработать RAG запрос"""
    logger.info(f"Processing RAG request for chat_id: {request.chat_id}")
    try:
        # Проверяем наличие OpenAI API ключа
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OpenAI API key not configured")
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key not configured"
            )
        
        logger.info(f"Processing user message: {request.user_message[:100]}...")
        
        # Обрабатываем RAG запрос
        result = rag_pipeline.process_rag_request(
            chat_id=request.chat_id,
            user_message=request.user_message,
            db_manager=db_manager
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

@app.get("/chat/{chat_id}/history")
async def get_chat_history(chat_id: str):
    """Получить историю чата"""
    logger.info(f"Getting chat history for chat_id: {chat_id}")
    try:
        messages = db_manager.get_chat_history(chat_id)
        logger.info(f"Retrieved {len(messages)} messages for chat_id: {chat_id}")
        return {
            "chat_id": chat_id,
            "messages": messages
        }
    except Exception as e:
        logger.error(f"Error retrieving chat history for chat_id {chat_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")

@app.get("/chat/{chat_id}/params")
async def get_chat_params(chat_id: str):
    """Получить параметры чата"""
    logger.info(f"Getting chat params for chat_id: {chat_id}")
    try:
        params = db_manager.get_chat_params(chat_id)
        if not params:
            logger.warning(f"Chat parameters not found for chat_id: {chat_id}")
            raise HTTPException(status_code=404, detail="Chat parameters not found")
        
        logger.info(f"Retrieved chat params for chat_id: {chat_id}")
        return {
            "chat_id": chat_id,
            "params": params
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chat params for chat_id {chat_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving chat params: {str(e)}")

# Кастомная функция для генерации OpenAPI схемы
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Добавляем дополнительные настройки для Swagger UI
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting RAG Service with uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=5060, log_level="info") 