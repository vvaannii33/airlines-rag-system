from fastapi import APIRouter, HTTPException
from app.schemas import QueryRequest, QueryResponse

router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    
    # validation already handled by Pydantic
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # dummy logic (replace later with RAG)
    answer = f"You asked: {request.query}"

    return QueryResponse(
        question=request.query,
        answer=answer
    )
