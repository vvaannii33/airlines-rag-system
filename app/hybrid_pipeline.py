from app.chains.sql_chain import SQLChain
from app.services.rag_pipeline import RAGPipeline
from app.services.router import QueryRouter
from app.schemas.response_models import HybridResponse
from app.utils.logger_config import logger
import time


class HybridPipeline:
    def __init__(self):
        self.sql_chain = SQLChain()
        self.rag = RAGPipeline()
        self.router = QueryRouter()

    def split_query(self, question:str):
        question_lower = question.lower()

        split_keywords = ["and","also",",","then","+","as well as","followed by"]

        for keyword in split_keywords:
            if keyword in question_lower:
                parts = question.split(keyword,1)
                return parts[0].strip(), parts[1].strip()
        return question, None

    def run(self, question: str):
        start_time = time.time()

        route = self.router.route(question)

        logger.info(f"[HYBRID_PIPELINE] Query routed to: {route}")

        if route == "mixed":
            logger.info(f"[HYBRID_PIPELINE] Mixed query detected. Splitting into SQL and RAG components...")
            sql_part, rag_part = self.split_query(question)

            sql_result = self.sql_chain.run(sql_part)
            rag_result = self.rag.run(rag_part)

            execution_time = round(time.time() - start_time,2)
            logger.info(f"[HYBRID_PIPELINE] Mixed query executed in {execution_time} seconds")
            return HybridResponse(
                source="mixed",
                sql=sql_result,
                rag=rag_result
            )

        elif route == "sql":
            execution_time = round(time.time() - start_time,2)
            logger.info(f"[HYBRID_PIPELINE] SQL query executed in {execution_time} seconds")
            return {
                "source" : "sql",
                "response" : self.sql_chain.run(question)
            }

        else:
            execution_time = round(time.time() - start_time,2)
            logger.info(f"[HYBRID_PIPELINE] RAG query executed in {execution_time} seconds")
            return {
                "source" : "rag",
                "response" : self.rag.run(question)
            }

