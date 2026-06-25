import sqlparse
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from app.utils.logger_config import logger
import time
from app.services.validator import SQLValidator
from app.services.query_executor import QueryExecutor
from app.prompts.sql_prompt import sql_prompt
from app.schemas.response_models import ErrorResponse
from app.exceptions.custom_exceptions import ValidationError, QueryExecutionError
from langchain_community.callbacks.manager import get_openai_callback

load_dotenv()

class SQLChain:
    def __init__(self):
        self.db = SQLDatabase.from_uri(os.getenv("LOCAL_DATABASE_URL"))

        self.schema = self.db.get_table_info()

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        self.parser = StrOutputParser()

        self.prompt = sql_prompt

        self.chain = self.prompt | self.llm | self.parser

        self.validator = SQLValidator()

        self.query_executor = QueryExecutor(db=self.db)
    

    def run(self, question: str):

        start_time = time.time()

        logger.info(f"[SQL_CHAIN] User question: {question}")

        with get_openai_callback() as cb:

            sql_query = self.chain.invoke({
            "question": question,
            "schema" : self.schema
            })
            execution_time = round(time.time() - start_time,2)

            logger.info(
            f"[TOKEN_USAGE][SQL] Prompt Tokens: {cb.prompt_tokens}"
            )

            logger.info(
            f"[TOKEN_USAGE][SQL] Completion Tokens: {cb.completion_tokens}"
            )

            logger.info(
            f"[TOKEN_USAGE][SQL] Total Tokens: {cb.total_tokens}"
            )

            logger.info(
            f"[TOKEN_USAGE][SQL] Total Cost (USD): ${cb.total_cost}"
            )

            if cb.total_cost > 0.00012:
                logger.warning(f"[SQL_CHAIN][HIGH_COST] High cost detected: ${cb.total_cost:.6f} for question: {question}")

            logger.info(
            f"[OBSERVABILITY][SQL] Tokens={cb.total_tokens} | Cost=${cb.total_cost} | Time={execution_time}s"
            )

            if cb.total_tokens > 3000:
                logger.warning(f"[SQL_CHAIN] High token usage detected: {cb.total_tokens} tokens for question: {question}")

        logger.info(f"[SQL_CHAIN] Generated SQL query: {sql_query}")      

        if sql_query.lower() == "invalid question":
            logger.warning(f"[SQL_CHAIN] Invalid question")
            return ErrorResponse(
                error="Invalid question",
                source="sql"
            )

        if sql_query.lower() == "please provide more details":
            logger.warning(f"[SQL_CHAIN] LLM Response: {sql_query}")
            return ErrorResponse(
                error="Please provide more details",
                source="sql"
            )
            

        allowed_tables = ["flights", "passengers", "bookings", "airports"]

        if not any(table in sql_query.lower() for table in allowed_tables):
            logger.warning(f"[SQL_CHAIN] Unknown tables referenced in query: {sql_query}")
            return ErrorResponse(
                error="Query references unknown tables.",
                source="sql"
            )

        logger.info(f"[SQL_CHAIN] Validating SQL query: {sql_query}")
        try:
            self.validator.validate_sql(sql_query)
        except ValidationError as e:
            logger.error(f"[SQL_CHAIN] Validation failed | Query: {sql_query} | Reason: {str(e)}")
            return ErrorResponse(
                error="Query validation failed",
                source="sql",
                details=str(e)
            )

        logger.info(f"[SQL_CHAIN] SQL query validated successfully. Executing query: {sql_query}")

        try:
            logger.info(f"[SQL_CHAIN] Query executing | Query: {sql_query}")
            return self.query_executor.query_executor(sql_query)
            query_execution_time = round(time.time() - start_time,2)
            logger.info(
            f"""
            ==================================================
            REQUEST SUMMARY
            ==================================================
            Question: {question}
            Route: SQL

            Execution Time: {execution_time:.2f}s

            Tokens: {total_tokens}
            Cost: ${cost:.6f}

            Status: SUCCESS
            ==================================================
            """
            )
        except QueryExecutionError as e:
            logger.warning(f"[SQL_CHAIN] Query execution error | Query: {sql_query} | Reason: {str(e)}")
            raise QueryExecutionError(str(e))