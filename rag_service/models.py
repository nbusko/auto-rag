from pydantic import BaseModel
from typing import List, Optional

class RAGRequest(BaseModel):
    chat_id: str
    user_message: str
    message_id: Optional[str] = None

class RAGResponse(BaseModel):
    chat_id: str
    message_id: str
    assistant_message: str
    retrieved_chunks: List[dict]
    similarity_scores: List[float]

class ChatContext(BaseModel):
    chat_id: str
    messages: List[dict]
    params: Optional[dict] = None

class RetrievedChunk(BaseModel):
    content: str
    chunk_index: int
    similarity: float 