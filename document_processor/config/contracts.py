from pydantic import BaseModel, Field
from typing import List, Annotated
from uuid import UUID


class DocumentRequest(BaseModel):
    document_id: UUID = Field(..., description="Уникальный идентификатор документа")
    split: Annotated[
        str,
        Field(
            description="Метод разбиения текста: 'llm' или 'batch'",
            pattern="^(llm|batch)$",
            examples=["llm", "batch"]
        )
    ]
    batch_size: Annotated[
        int,
        Field(
            default=None,
            description="Размер батча для обработки. Должен быть > 0 и <= 1000",
            ge=1,
            le=1000
        )
    ]


class DocumentResponse(BaseModel):
    document_id: UUID = Field(..., description="Уникальный идентификатор документа")
    texts: List[str] = Field(..., description="Список разбитых текстовых блоков")
    embeddings: List[List[float]] = Field(..., description="Список эмбеддингов, соответствующих текстовым блокам")
