import os
import uuid
import logging
import json
from typing import Optional, List, Self, Any
from uuid import UUID
from pydantic import Field
from pydantic import BaseModel
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from config.contracts import RAGResponse, Status
from config.rag_settings import AppConfig
from config.constants import FILTER_BAD_REQUEST_PROMPT, IS_BAD_ANSWER, IS_NO_ANSWER
from embedding_search import EmbeddingSearcher

logger = logging.getLogger(__name__)
app_config = AppConfig()

class RAGPipeline:
    def __init__(self, config: AppConfig = app_config):
        self.config = config
        logger.info("Initialized RAG Pipeline class")
        self.embedder = SentenceTransformer(self.config.EMBEDDER_MODEL)

    async def _init_llm(
        self,
        llm_model: str,
        temperature: float,
        prompt_retrieve: str,
        prompt_augmentation: str,
        prompt_generation: str,
    ) -> Self:
        logger.info("Initializing LangChain model and prompts")
        self.llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model_name=llm_model,
            temperature=temperature,
            base_url=str(self.config.OPENAI_BASE_URL),
        )
        # Prepare prompt templates
        self.filter_prompt = PromptTemplate(
            input_variables=["request"],
            template=FILTER_BAD_REQUEST_PROMPT,
        )
        self.retrieve_prompt = PromptTemplate(
            input_variables=["request"],
            template=prompt_retrieve,
        )
        self.map_reduce_prompt = PromptTemplate(
            input_variables=["request", "info"],
            template=prompt_augmentation,
        )
        self.generation_prompt = PromptTemplate(
            input_variables=["request", "info"],
            template=prompt_generation,
        )
        # Chains
        self.filter_chain = LLMChain(llm=self.llm, prompt=self.filter_prompt)
        self.retrieve_chain = LLMChain(llm=self.llm, prompt=self.retrieve_prompt)
        self.map_reduce_chain = LLMChain(llm=self.llm, prompt=self.map_reduce_prompt)
        self.generate_chain = LLMChain(llm=self.llm, prompt=self.generation_prompt)
        return self

    async def process_rag_request(
        self,
        chat_id: str,
        user_message: str,
        document_id: str,
        message_id: Optional[str],
        llm_model: str,
        prompt_retrieve: str,
        prompt_augmentation: str,
        prompt_generation: str,
        top_k: int,
        temperature: float,
        threshold: float,
        embeddings: List[List[float]],
        text_chunks: List[str],
    ) -> RAGResponse:
        try:
            # Initialize LLM and prompts
            await self._init_llm(llm_model, temperature, prompt_retrieve, prompt_augmentation, prompt_generation)

            # 1. Filter request
            logger.debug("Filtering user request")
            filter_output = await self.filter_chain.apredict(request=user_message)
            filter_json = json.loads(filter_output)
            if filter_json.get("result") != "yes":
                logger.warning("Request did not pass filter: %s", user_message)
                return RAGResponse(
                    status=Status.ERROR,
                    message="IS_BAD_ANSWER",
                    chat_id=chat_id,
                    message_id=message_id,
                    document_id=document_id,
                    generated_answer=IS_BAD_ANSWER
                )

            # 2. Transform user query
            logger.debug("Transforming user query")
            improved_query = await self.retrieve_chain.apredict(request=user_message)

            # 3. Embed query and search
            logger.debug("Embedding and searching for relevant chunks")
            query_emb = self.embedder.encode(improved_query, normalize_embeddings=True).tolist()
            searcher = EmbeddingSearcher(embeddings, text_chunks)
            raw_segments = searcher.search(query_emb, top_k, threshold)
            if not raw_segments:
                logger.info("No relevant segments found for query: %s", improved_query)
                return RAGResponse(
                    status=Status.ERROR,
                    message="IS_NO_ANSWER",
                    chat_id=chat_id,
                    message_id=message_id,
                    document_id=document_id,
                    generated_answer=IS_NO_ANSWER
                )

            # 4. Map-Reduce selection
            logger.debug("Applying map-reduce to select best segments")
            selected_segments: List[str] = []
            batch_size = 3
            for i in range(0, len(raw_segments), batch_size):
                batch = raw_segments[i : i + batch_size]
                info = "\n".join(batch)
                map_out = await self.map_reduce_chain.apredict(request=user_message, info=info)
                try:
                    picks = json.loads(map_out)
                    if isinstance(picks, list):
                        selected_segments.extend(picks)
                except json.JSONDecodeError:
                    logger.error("Map-reduce output is not valid JSON list: %s", map_out)
            if not selected_segments:
                logger.info("Map-reduce did not yield any segments")
                return RAGResponse(
                    status=Status.ERROR,
                    message="IS_NO_ANSWER",
                    chat_id=chat_id,
                    message_id=message_id,
                    document_id=document_id,
                    generated_answer=IS_NO_ANSWER
                )

            # 5. Generate final answer
            logger.debug("Generating final answer")
            info_for_gen = "\n".join(selected_segments)
            generated = await self.generate_chain.apredict(request=user_message, info=info_for_gen)

            return RAGResponse(
                status=Status.SUCCESS,
                message="OK",
                chat_id=chat_id,
                message_id=message_id,
                document_id=document_id,
                generated_answer=generated,
            )

        except Exception as e:
            logger.exception("Error processing RAG request: %s", e)
            return RAGResponse(
                status=Status.ERROR,
                message=str(e),
                chat_id=chat_id,
                message_id=message_id,
                document_id=document_id,
            )
