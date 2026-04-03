
# Project Audit – Vanathi Airlines RAG
_Last updated: April 2026_

This document evaluates the current state of the Airlines RAG project from a system design and production readiness perspective, 
identifying gaps and outlining improvements to reach production-grade GenAI system standards.

## 1. Current Functionality
- Airline Q&A chatbot using Retrieval-Augmented Generation (RAG)
- Handles queries on flights, bookings, policies
- Pipeline: Embedding → Vector Search → LLM → Response
- Built using LangChain + OpenAI + ChromaDB

---

## 2. Tech Stack
- Python 3.x
- LangChain (pre-LCEL usage)
- OpenAI API (GPT models)
- ChromaDB (vector store)
- Jupyter Notebook (current)
- Optional Streamlit/Gradio UI

---

## 3. System Design Gaps (Senior-Level View)

### Scalability
- No batching or async handling
- No caching (LLM responses / embeddings)
- No horizontal scaling strategy

### Reliability
- No retry mechanisms (LLM/API failures)
- No fallback models
- No circuit breaker or timeout handling

### Observability
- No tracing (LangSmith)
- No logs for:
  - latency
  - token usage
  - failures
- No alerting

### Cost Awareness
- No tracking of token usage
- No cost optimization (caching, model selection)

---

## 4. Retrieval & RAG Gaps

### Retrieval Quality
- Only semantic similarity (no hybrid BM25)
- No re-ranking layer
- No metadata filtering

### Context Quality
- Fixed chunking (no semantic chunking)
- No query rewriting
- No multi-hop retrieval

---

## 5. LLM / Generation Gaps

- No structured prompting (few-shot / templates)
- No hallucination control (grounded generation missing)
- No response validation layer
- No streaming responses

---

## 6. Architecture Gaps

- Notebook-based (non-modular)
- No API layer (FastAPI missing)
- No separation of:
  - retrieval
  - generation
  - evaluation
- Hardcoded configs (no env/config management)

---

## 7. Evaluation Gaps (CRITICAL)

- No automated evaluation
- No defined metrics:
  - Faithfulness
  - Answer relevance
  - Context recall
- No dataset for testing queries

---

## 8. Failure Modes (VERY IMPORTANT)

System may fail in cases like:
- Irrelevant retrieval → hallucinated answer
- Long/complex queries → incomplete context
- Ambiguous queries → wrong interpretation
- API failure → no fallback
- High latency → poor UX

---

## 9. Success Metrics (Add This for Interviews)

Target metrics after improvements:

- Faithfulness score > 0.85 (RAGAS)
- Answer relevance > 0.85
- Latency < 2.5 seconds
- Retrieval accuracy (top-k hit rate) > 80%
- Cost per query minimized via caching

---

## 10. Improvement Roadmap

### Phase 1 (Week 1–2): Foundation & Retrieval
- Migrate to LCEL + modular architecture
- Implement hybrid search (BM25 + embeddings)
- Add re-ranking (Cohere / cross-encoder)
- Introduce RAGAS evaluation

### Phase 2 (Week 2–3): Production Layer
- Build FastAPI backend
- Add streaming responses
- Add logging (latency, tokens, errors)
- Integrate LangSmith tracing
- Add retry + fallback mechanisms

### Phase 3 (Week 6–7): Deployment
- Dockerize application
- Deploy (Render / AWS / Azure)
- Add monitoring dashboard
- Write production-grade README + architecture diagram

---

## Final Goal

Transform from:
 "Basic RAG notebook project"

To:
"Production-ready, evaluated, observable RAG system with scalable architecture"

This demonstrates:
- System design thinking
- LLM application engineering
- Production readiness
