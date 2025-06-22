import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from typing import List
import uuid
from datetime import datetime

from models import HistoryItem, ParamsItem, DocItem, UpdateDocsRequest, ChatHistoryResponse
from database import DatabaseManager
from embedding_service import EmbeddingService

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('data_service.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Data Service", 
    version="1.0.0",
    description="Сервис для управления данными, эмбеддингами и историей чатов",
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
logger.info("Initializing Data Service...")
db_manager = DatabaseManager()
embedding_service = EmbeddingService()
logger.info("Data Service initialized successfully")

@app.on_event("startup")
async def startup_event():
    logger.info("Data Service starting up...")
    try:
        # Проверяем подключение к базе данных
        await db_manager.test_connection()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Data Service shutting down...")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Data Service is running", "docs": "/docs"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/chat/{chat_id}", response_model=ChatHistoryResponse)
async def get_chat_data(chat_id: str):
    """Получить данные чата: историю сообщений и параметры"""
    logger.info(f"Getting chat data for chat_id: {chat_id}")
    try:
        # Получаем историю сообщений
        history_data = db_manager.get_chat_history(chat_id)
        messages = [
            HistoryItem(
                chat_id=item["chat_id"],
                message_id=item["message_id"],
                message_role=item["message_role"],
                content=item["content"],
                timestamp=item["timestamp"]
            )
            for item in history_data
        ]
        
        # Получаем параметры чата
        params_data = db_manager.get_chat_params(chat_id)
        params = None
        if params_data:
            params = ParamsItem(
                chat_id=params_data["chat_id"],
                prompt_id=params_data["prompt_id"],
                document_id=params_data["document_id"],
                top_k=params_data["top_k"],
                temperature=params_data["temperature"],
                max_tokens=params_data["max_tokens"],
                model_name=params_data["model_name"]
            )
        
        logger.info(f"Retrieved chat data for chat_id: {chat_id}, messages: {len(messages)}")
        
        return ChatHistoryResponse(
            chat_id=chat_id,
            messages=messages,
            params=params
        )
    except Exception as e:
        logger.error(f"Error retrieving chat data for chat_id {chat_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving chat data: {str(e)}")

@app.post("/chat/{chat_id}/message")
async def add_message(chat_id: str, message: HistoryItem):
    """Добавить сообщение в чат"""
    logger.info(f"Adding message to chat_id: {chat_id}, role: {message.message_role}")
    try:
        if not message.message_id:
            message.message_id = str(uuid.uuid4())
        
        db_manager.add_message(
            chat_id=chat_id,
            message_id=message.message_id,
            message_role=message.message_role,
            content=message.content
        )
        
        logger.info(f"Message added successfully for chat_id: {chat_id}, message_id: {message.message_id}")
        return {"message": "Message added successfully", "message_id": message.message_id}
    except Exception as e:
        logger.error(f"Error adding message for chat_id {chat_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error adding message: {str(e)}")

@app.post("/chat/{chat_id}/params")
async def update_params(chat_id: str, params: ParamsItem):
    """Обновить параметры чата"""
    logger.info(f"Updating params for chat_id: {chat_id}")
    try:
        db_manager.update_params(
            chat_id=chat_id,
            prompt_id=params.prompt_id,
            document_id=params.document_id,
            top_k=params.top_k,
            temperature=params.temperature,
            max_tokens=params.max_tokens,
            model_name=params.model_name
        )
        
        logger.info(f"Parameters updated successfully for chat_id: {chat_id}")
        return {"message": "Parameters updated successfully"}
    except Exception as e:
        logger.error(f"Error updating parameters for chat_id {chat_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error updating parameters: {str(e)}")

@app.post("/docs/update")
async def update_docs(request: UpdateDocsRequest):
    """Обновить документы с эмбеддингами"""
    logger.info(f"Updating docs for document_id: {request.document_id}")
    try:
        # Обрабатываем документ: разбиваем на чанки и создаем эмбеддинги
        chunks = embedding_service.process_document(
            document_id=request.document_id,
            content=request.content,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        
        # Сохраняем в базу данных
        db_manager.update_docs(request.document_id, chunks)
        
        logger.info(f"Documents updated successfully for document_id: {request.document_id}, chunks: {len(chunks)}")
        
        return {
            "message": "Documents updated successfully",
            "document_id": request.document_id,
            "chunks_count": len(chunks)
        }
    except Exception as e:
        logger.error(f"Error updating documents for document_id {request.document_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error updating documents: {str(e)}")

@app.get("/docs/{document_id}/search")
async def search_docs(document_id: str, query: str, top_k: int = 5):
    """Поиск похожих чанков в документе"""
    logger.info(f"Searching docs for document_id: {document_id}, query: {query[:50]}...")
    try:
        # Получаем эмбеддинг для запроса
        query_embedding = embedding_service.get_embeddings([query])[0]
        
        # Ищем похожие чанки
        similar_chunks = db_manager.search_similar_chunks(
            query_embedding=query_embedding,
            document_id=document_id,
            top_k=top_k
        )
        
        logger.info(f"Search completed for document_id: {document_id}, found {len(similar_chunks)} results")
        
        return {
            "document_id": document_id,
            "query": query,
            "results": similar_chunks
        }
    except Exception as e:
        logger.error(f"Error searching documents for document_id {document_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

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
    logger.info("Starting Data Service with uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=5050, log_level="info") 