import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
import requests

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rag_user:rag_password@localhost:5432/rag_db")
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data_service:5050")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseManager:
    def __init__(self):
        self.engine = engine
        logger.info(f"DatabaseManager initialized with DATABASE_URL: {DATABASE_URL}")
        logger.info(f"DATA_SERVICE_URL: {DATA_SERVICE_URL}")
    
    async def test_connection(self):
        """Тестирование подключения к базе данных"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
    
    def get_chat_history(self, chat_id: str) -> List[dict]:
        """Получить историю чата через API data_service"""
        logger.info(f"Getting chat history for chat_id: {chat_id}")
        try:
            response = requests.get(f"{DATA_SERVICE_URL}/chat/{chat_id}")
            response.raise_for_status()
            data = response.json()
            messages = data.get("messages", [])
            logger.info(f"Retrieved {len(messages)} messages for chat_id: {chat_id}")
            return messages
        except requests.RequestException as e:
            logger.error(f"Error getting chat history for chat_id {chat_id}: {e}")
            return []
    
    def get_chat_params(self, chat_id: str) -> Optional[dict]:
        """Получить параметры чата через API data_service"""
        logger.info(f"Getting chat params for chat_id: {chat_id}")
        try:
            response = requests.get(f"{DATA_SERVICE_URL}/chat/{chat_id}")
            response.raise_for_status()
            data = response.json()
            params = data.get("params")
            logger.info(f"Retrieved chat params for chat_id: {chat_id}")
            return params
        except requests.RequestException as e:
            logger.error(f"Error getting chat params for chat_id {chat_id}: {e}")
            return None
    
    def add_message(self, chat_id: str, message_id: str, message_role: str, content: str):
        """Добавить сообщение в чат через API data_service"""
        logger.info(f"Adding message to chat_id: {chat_id}, role: {message_role}")
        try:
            message_data = {
                "chat_id": chat_id,
                "message_id": message_id,
                "message_role": message_role,
                "content": content
            }
            response = requests.post(f"{DATA_SERVICE_URL}/chat/{chat_id}/message", json=message_data)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Message added successfully for chat_id: {chat_id}")
            return result
        except requests.RequestException as e:
            logger.error(f"Error adding message for chat_id {chat_id}: {e}")
            return None
    
    def search_similar_chunks(self, query_embedding: List[float], document_id: str, top_k: int = 5) -> List[dict]:
        """Поиск похожих чанков по косинусному сходству"""
        logger.info(f"Searching similar chunks for document_id: {document_id}, top_k: {top_k}")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                        SELECT content, chunk_index, 1 - (embedding <=> :embedding) as similarity
                        FROM docs 
                        WHERE document_id = :document_id
                        ORDER BY embedding <=> :embedding
                        LIMIT :top_k
                    """),
                    {
                        "embedding": query_embedding,
                        "document_id": document_id,
                        "top_k": top_k
                    }
                )
                chunks = [dict(row) for row in result]
                logger.info(f"Found {len(chunks)} similar chunks for document_id: {document_id}")
                return chunks
        except Exception as e:
            logger.error(f"Error searching similar chunks for document_id {document_id}: {e}")
            return [] 