import logging
import json
import time
import uuid
from typing import List, Optional, Self
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from config.contracts import DocumentResponse, Status, SplitMethod
from config.app_settings import AppConfig
from sentence_transformers import SentenceTransformer
from config.constants import (
    EMBEDDING_ERROR_MESSAGE,
    PROCESSING_ERROR_MESSAGE,
    INVALID_FILE_TYPE_MESSAGE,
)
from utils import process_file, process_text

logger = logging.getLogger(__name__)
app_config = AppConfig()


class DocumentPipeline:
    def __init__(self, config: AppConfig = app_config):
        self.config = config
        self.embedder = SentenceTransformer(self.config.EMBEDDER_MODEL)
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

            if split_method == SplitMethod.LLM:
                await self._init_llm(llm_model, temperature, prompt_split, prompt_table)

            # Определяем тип файла и извлекаем содержимое
            file_type, data = await process_file(file_binary)
            logger.info(f"File type detected: {file_type}")

            if data == ["unknown"]:
                processing_time = time.time() - start_time
                return DocumentResponse(
                    status=Status.ERROR,
                    message=INVALID_FILE_TYPE_MESSAGE,
                    document_id=document_id,
                    texts=[],
                    embeddings=[],
                    chunks_count=0,
                    processing_time=processing_time,
                )

            if file_type != "xlsx":
                if split_method == SplitMethod.LLM:
                    logger.info("Splitting document with LLM")
                    texts = await self._split_by_llm(data, batch_size)
                else:
                    logger.info(
                        f"Splitting document with batch method, size: {batch_size}"
                    )
                    texts = await self._split_by_batch(data, batch_size)
            else:
                texts = data

            # Получаем эмбеддинги для всех фрагментов
            logger.info(f"Getting embeddings for {len(texts)} text chunks")
            embeddings = await self._get_embeddings(texts)

            processing_time = time.time() - start_time
            if embeddings is None:
                return DocumentResponse(
                    status=Status.ERROR,
                    message=EMBEDDING_ERROR_MESSAGE,
                    document_id=document_id,
                    texts=[],
                    embeddings=[],
                    chunks_count=0,
                    processing_time=processing_time,
                )

            logger.info(
                f"Document processing completed successfully. Chunks: {len(texts)}, Time: {processing_time:.2f}s"
            )

            return DocumentResponse(
                status=Status.SUCCESS,
                message="Document processed successfully",
                document_id=document_id,
                texts=texts,
                embeddings=embeddings,
                chunks_count=len(texts),
                processing_time=processing_time,
            )

        except Exception as e:
            processing_time = time.time() - start_time
            logger.exception(f"Error processing document {document_id}: {str(e)}")
            return DocumentResponse(
                status=Status.ERROR,
                message=f"{PROCESSING_ERROR_MESSAGE}: {str(e)}",
                document_id=document_id,
                processing_time=processing_time,
            )

    async def _process_table_with_llm(self, data: List[str]) -> List[str]:
        """
        Обрабатывает таблицу с помощью LLM
        """
        try:
            table_data = "\n".join(data)

            response = await self.table_chain.apredict(table_data=table_data)

            try:
                result = json.loads(response)
                if isinstance(result, list):
                    return [item.strip() for item in result if item.strip()]
            except json.JSONDecodeError:
                logger.warning("LLM response is not valid JSON, using fallback")
                # Fallback к простому разделению
                return await process_text(" ".join(data))

        except Exception as e:
            logger.error(f"Error processing table with LLM: {e}")
            # Fallback к простому разделению
            return await process_text(" ".join(data))

    async def _split_by_llm(self, data: List[str], batch_size: int) -> List[str]:
        """
        Разделяет документ на смысловые части с помощью LLM
        """
        try:
            responses = []
            for full_text in data:
                response = await self.split_chain.apredict(text=full_text)
                responses.append(response)

            parsing_result = []
            for response in responses:
                try:
                    result = json.loads(response)
                    if isinstance(result, list):
                        parsing_result.extend(
                            [item.strip() for item in result if item.strip()]
                        )
                except json.JSONDecodeError:
                    logger.warning("LLM response is not valid JSON, using fallback")
                    # Fallback к простому разделению
                    return await process_text(" ".join(data), batch_size)
            return parsing_result

        except Exception as e:
            logger.error(f"Error splitting with LLM: {e}")
            # Fallback к простому разделению
            return await process_text(" ".join(data), batch_size)

    async def _split_by_batch(self, data: List[str], batch_size: int) -> List[str]:
        """
        Разделяет документ на части по размеру
        """
        full_text = " ".join(data)
        return await process_text(full_text, batch_size)

    async def _get_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Получает эмбеддинги для списка текстов
        """
        try:
            embeddings = self.embedder.encode(texts, normalize_embeddings=True).tolist()
            logger.info("Succefully embedded text")
            return embeddings
        except Exception as e:
            logger.error(f"Error getting embeddings: {e}")
            return None
