from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from app.rag_pipeline import RAGPipeline
from app.schemas import QueryResponse

app = FastAPI()

pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

        result = pipeline.run(request.query)

        try:

            if not result.get("answer"):
                 raise HTTPException(status_code=404, detail ="No answer generated")

            if not result.get("context_docs"):
                raise HTTPException(status_code=404, detail ="No relevant documents found")
            

            return QueryResponse(
            question = request.query,
            answer = result["answer"],
            context_docs =result["context_docs"]
            )

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

@app.get("/health")
def health():
    return {"status": "ok"}

