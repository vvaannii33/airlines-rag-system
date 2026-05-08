from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from app.logger_config import logger
import time
from app.services.validator import SQLValidator
from app.services.query_executor import QueryExecutor
from app.prompts.sql_prompt import sql_prompt

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

        logger.info(f"User question: {question}")

        sql_query = self.chain.invoke({
            "question": question,
            "schema" : self.schema
        })

        logger.info(f"Generated SQL query: {sql_query}")      

        if sql_query.lower() == "invalid question":
            return ({
                "sql": None,
                "result": "Invalid question" })
            logger.warning("LLM returned invalid question")

        if sql_query.lower() == "please provide more details":
            return ({
                "sql": None,
                "result": "Please provide more details" })
            logger.warning(f"LLM Response: {sql_query}")


        allowed_tables = ["flights", "passengers", "bookings", "airports"]

        if not any(table in sql_query.lower() for table in allowed_tables):
            return {
                "sql": sql_query,
                "result": "Query references unknown tables."
            }

        is_valid, message = self.validator.validate_sql(sql_query)
        if not is_valid:
            logger.warning(f"Blocked Query: {sql_query}")
            logger.warning(f"Validation Result: {message}")
            return ({
                "sql" : sql_query,
                "result" : f"Query validation failed: {message}"
            })


        return self.query_executor.query_executor(sql_query)