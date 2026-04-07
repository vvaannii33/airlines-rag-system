from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import RAGPipeline
import asyncio

app = FastAPI()

pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
async def ask_question(request: QueryRequest):
    await asyncio.sleep(3)  #simulate delay
    result = pipeline.run(request.query)
    return {
        "message" : "done"
         }

@app.get("/")
def root():
    return {"message": "RAG API running"}
