import logging
import json
import time
import uuid
import re
from typing import List, Tuple, Optional, Self
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from config.contracts import DocumentResponse, Status, SplitMethod
from config.app_settings import AppConfig
from config.constants import (
    DOCUMENT_SPLIT_PROMPT, 
    TABLE_PROCESSING_PROMPT,
    EMBEDDING_ERROR_MESSAGE,
    PROCESSING_ERROR_MESSAGE,
    INVALID_FILE_TYPE_MESSAGE,
    FILE_READ_ERROR_MESSAGE
)
from utils import process_file

logger = logging.getLogger(__name__)
app_config = AppConfig()

class DocumentPipeline:
    def __init__(self, config: AppConfig = app_config):
        self.config = config
        logger.info("Initialized Document Pipeline class")

    async def _init_llm(
        self,
        llm_model: str,
        temperature: float,
        prompt_split: str,
        prompt_table: str,
    ) -> Self:
        logger.info("Initializing LangChain model and prompts")
        self.llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model_name=llm_model,
            temperature=temperature,
            base_url=str(self.config.OPENAI_BASE_URL),
        )
     
        self.split_prompt = PromptTemplate(
            input_variables=["text"],
            template=prompt_split,
        )
        self.table_prompt = PromptTemplate(
            input_variables=["table_data"],
            template=prompt_table,
        )
     
        self.split_chain = LLMChain(llm=self.llm, prompt=self.split_prompt)
        self.table_chain = LLMChain(llm=self.llm, prompt=self.table_prompt)
        return self

    async def process_document(
        self,
        file_binary: bytes,
        document_id: uuid.UUID,
        split_method: SplitMethod,
        batch_size: int,
        llm_model: str,
        temperature: float,
        prompt_split: str,
        prompt_table: str,
    ) -> DocumentResponse:
        start_time = time.time()
        
        try:
            logger.info(f"Processing document {document_id} with method {split_method}")
            
            # Инициализируем LLM если нужно
            if split_method == SplitMethod.LLM:
                await self._init_llm(llm_model, temperature, prompt_split, prompt_table)
            
            # Определяем тип файла и извлекаем содержимое
            file_type, data = await process_file(file_binary)
            logger.info(f"File type detected: {file_type}")
            
            # Обрабатываем в зависимости от типа файла
            if file_type == "xlsx":
                logger.info("Processing table data with LLM")
                texts = await self._process_table_with_llm(data)
            else:
                # Для остальных документов - применяем выбранный метод разделения
                if split_method == SplitMethod.LLM:
                    logger.info("Splitting document with LLM")
                    texts = await self._split_by_llm(data)
                else:  # batch
                    logger.info(f"Splitting document with batch method, size: {batch_size}")
                    texts = await self._split_by_batch(data, batch_size)
            
            # Получаем эмбеддинги для всех фрагментов
            logger.info(f"Getting embeddings for {len(texts)} text chunks")
            embeddings = await self._get_embeddings(texts)
            
            processing_time = time.time() - start_time
            
            logger.info(f"Document processing completed successfully. Chunks: {len(texts)}, Time: {processing_time:.2f}s")
            
            return DocumentResponse(
                status=Status.SUCCESS,
                message="Document processed successfully",
                document_id=document_id,
                texts=texts,
                embeddings=embeddings,
                chunks_count=len(texts),
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.exception(f"Error processing document {document_id}: {str(e)}")
            return DocumentResponse(
                status=Status.ERROR,
                message=f"{PROCESSING_ERROR_MESSAGE}: {str(e)}",
                document_id=document_id,
                processing_time=processing_time
            )

    async def _process_table_with_llm(self, data: List[str]) -> List[str]:
        """
        Обрабатывает таблицу с помощью LLM
        """
        try:
            # Объединяем данные таблицы
            table_data = "\n".join(data)
            
            # Используем LLM для обработки таблицы
            response = await self.table_chain.apredict(table_data=table_data)
            
            # Парсим JSON ответ
            try:
                result = json.loads(response)
                if isinstance(result, list):
                    return [item.strip() for item in result if item.strip()]
            except json.JSONDecodeError:
                logger.warning("LLM response is not valid JSON, using fallback")
                # Fallback к простому разделению
                return await self._simple_split(table_data)
                
        except Exception as e:
            logger.error(f"Error processing table with LLM: {e}")
            # Fallback к простому разделению
            return await self._simple_split(" ".join(data))

    async def _split_by_llm(self, data: List[str]) -> List[str]:
        """
        Разделяет документ на смысловые части с помощью LLM
        """
        try:
            # Объединяем все части документа
            full_text = " ".join(data)
            
            # Используем LLM для разделения на смысловые части
            response = await self.split_chain.apredict(text=full_text)
            
            # Парсим JSON ответ
            try:
                result = json.loads(response)
                if isinstance(result, list):
                    return [item.strip() for item in result if item.strip()]
            except json.JSONDecodeError:
                logger.warning("LLM response is not valid JSON, using fallback")
                # Fallback к простому разделению
                return await self._simple_split(full_text)
                
        except Exception as e:
            logger.error(f"Error splitting with LLM: {e}")
            # Fallback к простому разделению
            return await self._simple_split(" ".join(data))

    async def _split_by_batch(self, data: List[str], batch_size: int) -> List[str]:
        """
        Разделяет документ на части по размеру
        """
        full_text = " ".join(data)
        return await self._simple_split(full_text, batch_size)

    async def _simple_split(self, text: str, max_length: int = 1000) -> List[str]:
        """
        Простое разделение текста по размеру
        """
        parts = []
        current_part = []
        current_length = 0
        
        # Разделяем по предложениям для лучшего качества
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            if current_length + len(sentence) > max_length and current_part:
                parts.append(" ".join(current_part))
                current_part = []
                current_length = 0
            
            current_part.append(sentence)
            current_length += len(sentence)
        
        if current_part:
            parts.append(" ".join(current_part))
        
        return parts

    async def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Получает эмбеддинги для списка текстов
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.config.OPENAI_API_KEY,
                base_url=str(self.config.OPENAI_BASE_URL)
            )
            
            response = client.embeddings.create(
                model=self.config.EMBEDDER_MODEL,
                input=texts
            )
            
            return [embedding.embedding for embedding in response.data]
            
        except Exception as e:
            logger.error(f"Error getting embeddings: {e}")
            # Возвращаем пустые эмбеддинги в случае ошибки
            return [[0.0] * 312 for _ in texts]  # 312 - размерность для text-embedding-3-small 