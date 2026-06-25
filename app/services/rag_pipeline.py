from app.services.retriever import Retriever
from app.chains.lcel_chain import LLMService
from app.schemas.response_models import RAGResponse
from app.utils.logger_config import logger
import time
from app.exceptions.custom_exceptions import RetrievalError
from langchain_community.callbacks.manager import get_openai_callback
import uuid


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.chain = LLMService()

    def run(self, query: str):
        total_start_time = time.time()
        """
        Full RAG pipeline:
        1. Retrieve docs
        2. Build context
        3. Generate answer
        """

        #retrieve relevant docs based on query
        try:
            logger.info(f"[RAG_PIPELINE] Running RAG retrieval for query: {query}")
            retrieval_start_time = time.time()
            request_id = str(uuid.uuid4())[:8]
            logger.info(f"[RAG_PIPELINE] Request ID: {request_id} | Starting document retrieval for RAG pipeline...")
            docs = self.retriever.get_relevant_docs(query)
            retrieval_time = round(time.time() - retrieval_start_time,2)
            logger.info(f"[RAG_PIPELINE] Request ID: {request_id} | Retrieved {len(docs)} relevant documents in {retrieval_time} seconds for RAG pipeline")
            if not docs:
                return RAGResponse(
                answer="No relevant information found.",
                context_docs=[],
                retrieval_time=retrieval_time,
                generation_time=0,
                total_time=0           
)

        except RetrievalError as e:
            logger.error(f"[RAG_PIPELINE] Error retrieving relevant documents for query: {query} | Error: {str(e)}")
            raise

        #convert docs to context string for LLM input
        context = "\n\n".join(f"Document {i+1} : {doc.page_content}" for i,doc in enumerate(docs))

        #LCEL call to generate answer
        with get_openai_callback() as cb:
            generation_start_time = time.time()
            response = self.chain.generate(context, query,request_id)
            generation_time = round(time.time() - generation_start_time,2)

            if cb.total_cost > 0.00012:
                logger.warning(f"[RAG_PIPELINE][HIGH_COST] High cost detected: ${cb.total_cost:.6f} for query: {query}")
        
        logger.info(f"[RAG_PIPELINE] RAG answer generated successfully")

        cleaned_answer = response.replace("\n", " ").replace("\\n", " ").strip()
        cleaned_docs = [" ".join(doc.page_content.replace("\n", " ").replace("\\n", " ").split()) for doc in docs]

        total_time = round(time.time() - total_start_time,2)
        if total_time > 3:
            logger.warning(f"[RAG_PIPELINE][SLOW_REQUEST] High latency detected: {total_time} seconds for query: {query}")
        logger.info(
        f"""
        ==================================================
        REQUEST SUMMARY
        ==================================================
        Question: {query}
        Request ID: {request_id}
        Retrieved Documents: {len(docs)}
        Route: RAG

        Retrieval Time: {retrieval_time:.2f}s
        Generation Time: {generation_time:.2f}s
        Total Time: {total_time:.2f}s

        Prompt Tokens: {cb.prompt_tokens}
        Completion Tokens: {cb.completion_tokens}
        Total Tokens: {cb.total_tokens}
        Cost: ${cb.total_cost:.6f}

        Status: SUCCESS
        ==================================================
        """
        )

        return RAGResponse(
            answer=cleaned_answer,
            context_docs=cleaned_docs,
            retrieval_time = retrieval_time,
            generation_time = generation_time,
            total_time = total_time,
            total_tokens = cb.total_tokens,
            cost = cb.total_cost
        )