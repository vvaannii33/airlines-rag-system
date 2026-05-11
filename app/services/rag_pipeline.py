from app.services.retriever import Retriever
from app.schemas import QueryResponse
from app.chains.lcel_chain import LLMService
from app.schemas.response_models import RAGResponse
from app.utils.logger_config import logger
import time
from app.exceptions.custom_exceptions import RetrievalError


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.chain = LLMService()

    def run(self, query: str):
        """
        Full RAG pipeline:
        1. Retrieve docs
        2. Build context
        3. Generate answer
        """

        #retrieve relevant docs based on query
        try:

            logger.info(f"[RAG_PIPELINE] Running RAG retrieval for query: {query}")
            start_time = time.time()
            docs = self.retriever.get_relevant_docs(query)
            retrieval_time = round(time.time() - start_time,2)
            logger.info(f"[RAG_PIPELINE] Retrieved {len(docs)} relevant documents in {retrieval_time} seconds for RAG pipeline")

        except RetrievalError as e:
            logger.error(f"[RAG_PIPELINE] Error retrieving relevant documents for query: {query} | Error: {str(e)}")
            raise

        #convert docs to context string for LLM input
        context = "\n\n".join(f"Document {i+1} : {doc}" for i,doc in enumerate(docs))

        #LCEL call to generate answer
        response = self.chain.generate(context, query)
        generation_time = round(time.time() - start_time,2)
        logger.info(f"[RAG_PIPELINE] RAG answer generated successfully")

        cleaned_answer = response.replace("\n", " ").replace("\\n", " ").strip()
        cleaned_docs = [" ".join(doc.replace("\n", " ").replace("\\n", " ").split()) for doc in docs]

        total_time = round(time.time() - start_time,2)
        logger.info(f"[RAG_PIPELINE] Total RAG pipeline execution time: {total_time} seconds")
        return RAGResponse(
            answer=cleaned_answer,
            context_docs=cleaned_docs
        )

        
