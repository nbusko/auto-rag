from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from uuid import UUID
from config.rag_settings import AppConfig
from config.constants import MAP_REDUCE_PROMPT, GENERATE_FINAL_ANSWER_PROMPT, RETRIEVE_PROMPT

config = AppConfig()

class RAGRequest(BaseModel):
    chat_id: str = Field(..., description="ID чата пользователя")
    user_message: str = Field(..., description="Текст сообщения от пользователя")
    message_id: Optional[str] = Field(
        default=None, description="Необязательный ID конкретного сообщения"
    )

    prompt_retrieve: Optional[str] = Field(
        default=RETRIEVE_PROMPT,
        description="Промпт для retrieval"
    )
    prompt_augmentation: Optional[str] = Field(
        default=MAP_REDUCE_PROMPT,
        description="Промпт для расширения запроса"
    )
    prompt_generation: Optional[str] = Field(
        default=GENERATE_FINAL_ANSWER_PROMPT,
        description="Промпт для генерации ответа"
    )

    top_k: Optional[int] = Field(
        default=12,
        ge=1,
        description="Сколько документов возвращает retriever"
    )
    temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Температура генерации LLM"
    )
    threshold: Optional[float] = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Порог для фильтрации по similarity"
    )

    document_id: UUID = Field(..., description="ID документов, к которым привязан чат/пользователь")

    llm: Optional[str] = Field(
        default="gpt-4o-mini",
        description="Имя LLM, используемой для генерации"
    )
    
    embeddings: Optional[List[List[float]]] = Field(
        ...,
        description="Список эмбеддингов для поиска похожих документов"
    )

    text_chunks: Optional[List[str]] = Field(
        ...,
        description="Список отрывков текста, связанных с эмбеддингами"
    )

class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class RAGResponse(BaseModel):
    status: Status = Field(..., description="Статус выполнения запроса (success/error)")
    message: str = Field(..., description="Сообщение со скриптом результата")
    chat_id: str = Field(..., description="ID чата пользователя из запроса")
    message_id: Optional[str] = Field(
        default=None, 
        description="ID сообщения из запроса, если был указан"
    )
    document_id: str = Field(..., description="ID документа из запроса")
    
    generated_answer: Optional[str] = Field(
        default=None,
        description="Сгенерированный ответ системы"
    )
