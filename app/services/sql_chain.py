from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from app.logger_config import logger
import time
from app.services.validator import SQLValidator
from app.services.query_executor import QueryExecutor

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

        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert PostgreSQL SQL generator.

        Here is the database schema:

        {schema}

        Convert the following question into a valid SQL query.

        Rules:
        - Only use the tables and columns from schema.
        - Use proper joins where required.
        - Return ONLY raw SQL.
        - Do NOT use markdown (no ```) or linebreaks.
        - Use JOINs when data spans multiple tables.
        - Understand relationships between tables.
        - Display only the relevant and similar columns in the result.
        - When a specific question is asked with a condition, use the where clause ONLY on the condition asked.
        - When filtering by time only (e.g., "after 10 AM"), extract and compare only the time component from datetime columns.
        - If the questions mentions only after or before with a time, compare only with the greater or lesser time component of the datetime column respectively.
        - When both date and time are mentioned, use full datetime comparison.
        - If the question does not make sense or is out of context, return "Invalid question". Do NOT attempt to answer it from the context.
        - If the question is ambiguous or lacks details, return "Please provide more details"
        - If the user asks to add data → generate INSERT query
        - If the user asks to modify data → generate UPDATE query
        - If the user asks to remove data → generate DELETE query
        - If the user asks to truncate data → generate TRUNCATE query
        - If the user asks to add/delete columns or change datatype of column(s) or modify name of column(s) in an existing table → generate ALTER query
        - If the user asks to drop a table → generate DROP query

        Question:
        {question}
        """)

        self.parser = StrOutputParser()

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