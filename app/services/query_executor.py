from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from app.logger_config import logger
import time

class QueryExecutor:

    def __init__(self, db):
        self.query_tool = QuerySQLDataBaseTool(db=db)

    def query_executor(self, sql_query: str):
        start_time = time.time()
        try:
            result = self.query_tool.invoke(sql_query)

            logger.info("SQL query executed successfully")
            logger.info(f"Query Result: {result}")

            if result == [] or result is None or (isinstance(result,str) and result.strip() == ""):
                
                return ({
                    "sql" : sql_query,
                    "result" : "No relevant data found for this query."
                })
                logger.info("Query returned no results")

        except Exception as e:
            return ({
                "sql" : sql_query,
                "result" : f"Invalid query. Please check your question and try again. Error: {str(e)}"
            })
            logger.error(f"Execution Error: {str(e)}")

        sql_query = sql_query.replace("```sql","").replace("```","").strip() 

        sql_query = sql_query.strip().rstrip(";")

        execution_time = round(time.time() - start_time,2)
        logger.info(f"Execution time: {execution_time} seconds")


        return {
            "sql": sql_query,
            "result": result
        }