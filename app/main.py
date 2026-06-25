from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from app.hybrid_pipeline import HybridPipeline
from app.services.rag_pipeline import RAGPipeline
from app.schemas.response_models import QueryResponse,SQLResponse
import uuid
from fastapi.responses import StreamingResponse
from app.utils.logger_config import logger
import time

request_counter = {}

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Airlines RAG API",
    version="1.0.0",
    description="RAG-powered AI Question Answering System"
)

pipeline = HybridPipeline()


class QueryRequest(BaseModel):
    query: str


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):

    try:
        request_id = str(uuid.uuid4())[:8]
        print(f"\n[REQUEST ID: {request_id}] Received query: {request.query}")

        client_ip = "local"

        current_time = time.time()

        if client_ip not in request_counter:
            request_counter[client_ip] = []

        request_counter[client_ip] = [
        t for t in request_counter[client_ip]
        if current_time - t < 60
        ]

        if len(request_counter[client_ip]) >= 10:
            logger.warning(f"[RATING] Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later."
            )

        request_counter[client_ip].append(current_time)

        result = pipeline.run(request.query,request_id)
        

        source = result["source"]
        response = result["response"]
        

        if source =="sql":
            return SQLResponse(
                sql=request.query,
                result=response
            )

        elif source == "rag":

            if not response.answer:
                raise HTTPException(
                    status_code=404,
                    detail="No answer generated"
                )

            if not response.context_docs:
                raise HTTPException(
                    status_code=404,
                    detail="No relevant documents found"
                )

            return QueryResponse(
                question=request.query,
                answer=response.answer,
                context_docs=response.context_docs
            )

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Network Error"
        )

    except TimeoutError:
        raise HTTPException(
            status_code=408,
            detail="Request timed out"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Error: " + str(e)
        )
'''
def fake_stream():

    for word in [
        "Hello ",
        "this ",
        "is ",
        "a ",
        "streaming ",
        "response."
    ]:
        yield word
        print(f"Streaming: {word.strip()}")
        time.sleep(0.05)
'''

@app.get("/")
def root():
    return {
        "message": "RAG API running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/stream")
def stream():

    return StreamingResponse(
        fake_stream(),
        media_type="text/plain"
    )