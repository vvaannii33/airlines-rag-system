from pydantic import BaseModel
from typing import Any, List, Optional

class SQLResponse(BaseModel):
    sql : Optional[str]
    result : Any

class RAGResponse(BaseModel):
    answer: str
    context_docs: List[str]

class HybridResponse(BaseModel):
    source: str
    sql: SQLResponse
    rag: RAGResponse

class ErrorResponse(BaseModel):
    error: str
    source: str | None = None
    details: str | None = None

