from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import RAGPipeline

app = FastAPI()

pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_question(request: QueryRequest):
    result = pipeline.run(request.query)
    return {
        "question": request.query,
        "answer": result["answer"]
         }

@app.get("/")
def root():
    return {"message": "RAG API running"}
   
