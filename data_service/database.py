import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
import numpy as np

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rag_user:rag_password@localhost:5432/rag_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseManager:
    def __init__(self):
        self.engine = engine
        logger.info(f"DatabaseManager initialized with DATABASE_URL: {DATABASE_URL}")
    
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
        """Получить историю чата"""
        logger.info(f"Getting chat history for chat_id: {chat_id}")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM history WHERE chat_id = :chat_id ORDER BY timestamp"),
                    {"chat_id": chat_id}
                )
                messages = [dict(row) for row in result]
                logger.info(f"Retrieved {len(messages)} messages for chat_id: {chat_id}")
                return messages
        except Exception as e:
            logger.error(f"Error getting chat history for chat_id {chat_id}: {e}")
            return []
    
    def get_chat_params(self, chat_id: str) -> Optional[dict]:
        """Получить параметры чата"""
        logger.info(f"Getting chat params for chat_id: {chat_id}")
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM params WHERE chat_id = :chat_id ORDER BY updated_at DESC LIMIT 1"),
                    {"chat_id": chat_id}
                )
                row = result.fetchone()
                params = dict(row) if row else None
                logger.info(f"Retrieved chat params for chat_id: {chat_id}")
                return params
        except Exception as e:
            logger.error(f"Error getting chat params for chat_id {chat_id}: {e}")
            return None
    
    def add_message(self, chat_id: str, message_id: str, message_role: str, content: str):
        """Добавить сообщение в историю"""
        logger.info(f"Adding message to chat_id: {chat_id}, role: {message_role}")
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                        INSERT INTO history (chat_id, message_id, message_role, content)
                        VALUES (:chat_id, :message_id, :message_role, :content)
                        ON CONFLICT (chat_id, message_id) DO UPDATE SET
                        content = EXCLUDED.content,
                        timestamp = CURRENT_TIMESTAMP
                    """),
                    {
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "message_role": message_role,
                        "content": content
                    }
                )
                conn.commit()
                logger.info(f"Message added successfully for chat_id: {chat_id}")
        except Exception as e:
            logger.error(f"Error adding message for chat_id {chat_id}: {e}")
            raise
    
    def update_params(self, chat_id: str, prompt_id: str, document_id: str, 
                     top_k: int = 5, temperature: float = 0.7, 
                     max_tokens: int = 1000, model_name: str = "gpt-3.5-turbo"):
        """Обновить параметры чата"""
        logger.info(f"Updating params for chat_id: {chat_id}")
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                        INSERT INTO params (chat_id, prompt_id, document_id, top_k, temperature, max_tokens, model_name)
                        VALUES (:chat_id, :prompt_id, :document_id, :top_k, :temperature, :max_tokens, :model_name)
                        ON CONFLICT (chat_id) DO UPDATE SET
                        prompt_id = EXCLUDED.prompt_id,
                        document_id = EXCLUDED.document_id,
                        top_k = EXCLUDED.top_k,
                        temperature = EXCLUDED.temperature,
                        max_tokens = EXCLUDED.max_tokens,
                        model_name = EXCLUDED.model_name,
                        updated_at = CURRENT_TIMESTAMP
                    """),
                    {
                        "chat_id": chat_id,
                        "prompt_id": prompt_id,
                        "document_id": document_id,
                        "top_k": top_k,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "model_name": model_name
                    }
                )
                conn.commit()
                logger.info(f"Parameters updated successfully for chat_id: {chat_id}")
        except Exception as e:
            logger.error(f"Error updating parameters for chat_id {chat_id}: {e}")
            raise
    
    def update_docs(self, document_id: str, chunks: List[dict]):
        """Обновить документы с эмбеддингами"""
        logger.info(f"Updating docs for document_id: {document_id}, chunks: {len(chunks)}")
        try:
            with self.engine.connect() as conn:
                # Удаляем старые чанки для данного документа
                conn.execute(
                    text("DELETE FROM docs WHERE document_id = :document_id"),
                    {"document_id": document_id}
                )
                
                # Добавляем новые чанки
                for chunk in chunks:
                    conn.execute(
                        text("""
                            INSERT INTO docs (document_id, chunk_index, content, embedding)
                            VALUES (:document_id, :chunk_index, :content, :embedding)
                        """),
                        {
                            "document_id": document_id,
                            "chunk_index": chunk["chunk_index"],
                            "content": chunk["content"],
                            "embedding": chunk["embedding"]
                        }
                    )
                conn.commit()
                logger.info(f"Documents updated successfully for document_id: {document_id}")
        except Exception as e:
            logger.error(f"Error updating documents for document_id {document_id}: {e}")
            raise
    
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