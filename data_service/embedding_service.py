import re
import logging
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info("Initializing Embedding Service...")
        # Загружаем модель rubert-tiny-turbo
        logger.info("Loading embedding model: sergeyzh/rubert-mini-frida")
        self.model = SentenceTransformer('sergeyzh/rubert-mini-frida')
        logger.info("Embedding Service initialized successfully")
    
    def chunk_text(self, text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        """Разбивает текст на чанки"""
        logger.info(f"Chunking text, length: {len(text)}, chunk_size: {chunk_size}, overlap: {chunk_overlap}")
        
        if len(text) <= chunk_size:
            logger.info("Text is shorter than chunk_size, returning as single chunk")
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Если это не последний чанк, пытаемся найти границу предложения
            if end < len(text):
                # Ищем ближайший конец предложения
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
                else:
                    # Ищем ближайший пробел
                    space_pos = text.rfind(' ', start, end)
                    if space_pos > start + chunk_size // 2:
                        end = space_pos + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - chunk_overlap
            if start >= len(text):
                break
        
        logger.info(f"Text chunked into {len(chunks)} chunks")
        return chunks
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Получает эмбеддинги для списка текстов"""
        logger.info(f"Getting embeddings for {len(texts)} texts")
        
        if not texts:
            logger.warning("No texts provided for embedding")
            return []
        
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def process_document(self, document_id: str, content: str, 
                        chunk_size: int = 500, chunk_overlap: int = 50) -> List[dict]:
        """Обрабатывает документ: разбивает на чанки и создает эмбеддинги"""
        logger.info(f"Processing document: {document_id}, content length: {len(content)}")
        
        try:
            # Разбиваем текст на чанки
            chunks = self.chunk_text(content, chunk_size, chunk_overlap)
            
            # Получаем эмбеддинги для всех чанков
            embeddings = self.get_embeddings(chunks)
            
            # Формируем результат
            result = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                result.append({
                    "document_id": document_id,
                    "chunk_index": i,
                    "content": chunk,
                    "embedding": embedding
                })
            
            logger.info(f"Document {document_id} processed successfully: {len(result)} chunks created")
            return result
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            raise 