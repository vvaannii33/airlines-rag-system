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

load_dotenv()

class SQLChain:
    def __init__(self):
        self.db = SQLDatabase.from_uri(
            "postgresql+psycopg2://admin:admin@localhost:5432/airlines"
        )

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

        sql_query = self.chain.invoke({
            "question": question,
            "schema" : self.schema
        })

        logger.info(f"[SQL_CHAIN] Generated SQL query: {sql_query}")      

        if sql_query.lower() == "invalid question":
            logger.warning(f"[SQL_CHAIN] LLM returned invalid question")
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
            logger.warning(f"[SQL_CHAIN] Validation failed | Query: {sql_query} | Reason: {str(e)}")
            return ErrorResponse(
                error="Query validation failed",
                source="sql",
                details=str(e)
            )

        logger.info(f"[SQL_CHAIN] SQL query validated successfully. Executing query: {sql_query}")

        try:
            return self.query_executor.query_executor(sql_query)
        except QueryExecutionError as e:
            logger.warning(f"[SQL_CHAIN] Query execution error | Query: {sql_query} | Reason: {str(e)}")
            raise QueryExecutionError(str(e))