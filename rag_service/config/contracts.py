from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from uuid import UUID
from config.rag_settings import AppConfig

config = AppConfig()

class RAGRequest(BaseModel):
    chat_id: str = Field(..., description="ID чата пользователя")
    user_message: str = Field(..., description="Текст сообщения от пользователя")
    message_id: Optional[str] = Field(
        default=None, description="Необязательный ID конкретного сообщения"
    )

    prompt_retrieve: Optional[str] = Field(
        default=config.prompt_retrieve,
        description="Промпт для retrieval"
    )
    prompt_augmentation: Optional[str] = Field(
        default=config.prompt_augmentation,
        description="Промпт для расширения запроса"
    )
    prompt_generation: Optional[str] = Field(
        default=config.prompt_generation,
        description="Промпт для генерации ответа"
    )

    top_k: Optional[int] = Field(
        default=config.top_k,
        ge=1,
        description="Сколько документов возвращает retriever"
    )
    temperature: Optional[float] = Field(
        default=config.temperature,
        ge=0.0,
        le=1.0,
        description="Температура генерации LLM"
    )
    threshold: Optional[float] = Field(
        default=config.threshold,
        ge=0.0,
        le=1.0,
        description="Порог для фильтрации по similarity"
    )

    document_id: UUID = Field(..., description="ID документов, к которым привязан чат/пользователь")
    llm: Optional[str] = Field(
        default=config.llm,
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
    message: str = Field(..., description="Сообщение с ответом или описанием ошибки")
    chat_id: str = Field(..., description="ID чата пользователя из запроса")
    message_id: Optional[str] = Field(
        default=None, 
        description="ID сообщения из запроса, если был указан"
    )
    document_id: str = Field(..., description="ID документа из запроса")
    
    # retrieved_texts: Optional[list[str]] = Field(
    #     default=None,
    #     description="Список найденных релевантных отрывков текста"
    # )

    generated_answer: Optional[str] = Field(
        default=None,
        description="Сгенерированный ответ системы"
    )
    # debug_info: Optional[dict] = Field(
    #     default=None,
    #     description="Дополнительная отладочная информация"
    # )
