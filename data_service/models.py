from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HistoryItem(BaseModel):
    chat_id: str
    message_id: str
    message_role: str
    content: str
    timestamp: Optional[datetime] = None

class ParamsItem(BaseModel):
    chat_id: str
    prompt_id: str
    document_id: str
    top_k: int = 5
    temperature: float = 0.7
    max_tokens: int = 1000
    model_name: str = "gpt-3.5-turbo"

class DocItem(BaseModel):
    document_id: str
    chunk_index: int
    content: str
    embedding: Optional[List[float]] = None

class UpdateDocsRequest(BaseModel):
    document_id: str
    content: str
    chunk_size: int = 500
    chunk_overlap: int = 50

class ChatHistoryResponse(BaseModel):
    chat_id: str
    messages: List[HistoryItem]
    params: Optional[ParamsItem] = None 