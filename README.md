# Airlines RAG System
Vanathi Airlines RAG System is a GenAI application that answers airline queries using RAG. It combines vector search (ChromaDB) with LLMs (OpenAI) to generate context-aware responses. Built with a modular FastAPI backend, it focuses on retrieval quality, evaluation, and production readiness.

## Overview
RAG-based Q&A system for airline policies.

## Features
- Retrieval-Augmented Generation (RAG)
- Context-aware responses using vector search
- Modular backend design (Retriever + LLM separation)
- Error handling and validation

## Tech Stack
- FastAPI
- LangChain
- ChromaDB
- OpenAI

## Architecture
User → API → RAG Pipeline → Retriever + LLM → Response

## API Endpoints

- POST /ask  
  Request:
  {
    "query": "What is probation?"
  }

  Response:
  {
    "question": "...",
    "answer": "..."
  }

- GET /  
  Health check endpoint

## How to run
1. Clone repo
2. Create venv
3. pip install -r requirements.txt
4. Add OPENAI_API_KEY
5. uvicorn app.main:app --reload


  ## Future Improvements
- Async pipeline for scalability
- Hybrid search (BM25 + vector)
- Reranking for better accuracy
- Frontend UI (React/Streamlit)