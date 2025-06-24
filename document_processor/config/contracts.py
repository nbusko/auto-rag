from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from enum import Enum
from config.app_settings import AppConfig
from config.constants import DOCUMENT_SPLIT_PROMPT, TABLE_PROCESSING_PROMPT

config = AppConfig()


class SplitMethod(str, Enum):
    LLM = "llm"
    BATCH = "batch"


class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class DocumentRequest(BaseModel):
    document_id: UUID = Field(..., description="Уникальный идентификатор документа")
    split_method: Optional[SplitMethod] = Field(
        default=SplitMethod.BATCH,
        description="Метод разбиения текста: 'llm' или 'batch'",
    )
    batch_size: Optional[int] = Field(
        default=1000,
        ge=5,
        le=2000,
        description="Размер батча для обработки (для batch метода)",
    )
    llm_model: Optional[str] = Field(
        default="gpt-4o-mini", description="Модель LLM для разделения документов"
    )
    temperature: Optional[float] = Field(
        default=0.1, ge=0.0, le=1.0, description="Температура для LLM генерации"
    )
    prompt_split: Optional[str] = Field(
        default=DOCUMENT_SPLIT_PROMPT, description="Промпт для разделения документа"
    )
    prompt_table: Optional[str] = Field(
        default=TABLE_PROCESSING_PROMPT, description="Промпт для обработки таблиц"
    )


class DocumentResponse(BaseModel):
    status: Status = Field(..., description="Статус выполнения запроса")
    message: str = Field(..., description="Сообщение о результате обработки")
    document_id: UUID = Field(..., description="Уникальный идентификатор документа")
    texts: Optional[List[str]] = Field(
        default=None, description="Список разбитых текстовых блоков"
    )
    embeddings: Optional[List[List[float]]] = Field(
        default=None, description="Список эмбеддингов, соответствующих текстовым блокам"
    )
    chunks_count: Optional[int] = Field(
        default=None, description="Количество созданных чанков"
    )
    processing_time: Optional[float] = Field(
        default=None, description="Время обработки в секундах"
    )
