from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from app.rag_pipeline import RAGPipeline

app = FastAPI()

pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail ="Query cannot be empty")

        result = pipeline.run(request.query)

        if not result["answer"]:
            raise HTTPException(status_code=404, detail ="No answer generated")

        if not result["context_docs"]:
            raise HTTException(status_code=404, detail ="No relevant documents found")

        return {
            "question" : request.query,
            "answer" : result["answer"]
         }

        except ConnectionError:
            raise HTTPException(status_code=503, detail ="Network Error")

        except TimeoutError:
            raise HTTPException(status_code=408, detail ="Request timed out")


    except HTTPException:
        raise 


    except Exception as e:
        raise HTTPException(status_code=500, detail ="Internal Error:" + str(e))

@app.get("/")
def root():
    return {"message": "RAG API running"}

@app.get("/health"):
def health():
    return {"status": "ok"}

