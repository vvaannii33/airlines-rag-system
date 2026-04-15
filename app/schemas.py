from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)

@field_validator("query")
def no_empty_spaces(cls, v):
    if not v.strip():
        raise ValueError("Query cannot be empty or spaces")
        return v    

class QueryResponse(BaseModel):
    question: str
    answer: str
    context_docs: list[str]
