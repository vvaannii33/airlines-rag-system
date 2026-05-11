from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from app.utils.logger_config import logger
import time
from app.schemas.response_models import SQLResponse, ErrorResponse

class QueryExecutor:

    def __init__(self, db):
        self.query_tool = QuerySQLDataBaseTool(db=db)

    def query_executor(self, sql_query: str):
        start_time = time.time()
        try:
            result = self.query_tool.invoke(sql_query)
            execution_time = round(time.time() - start_time,2)
            logger.info(f"[QUERY_EXECUTOR] Execution time: {execution_time} seconds")
            logger.info(f"[QUERY_EXECUTOR] SQL query executed successfully")
            logger.info(f"[QUERY_EXECUTOR] Query Result: {result}")

            if result == [] or result is None or (isinstance(result,str) and result.strip() == ""):

                logger.info("[QUERY_EXECUTOR] Query returned no results")
                return ErrorResponse(
                    error="No relevant data found for this query.",
                    source="sql"
                )

        except Exception as e:
            logger.error(f"[QUERY_EXECUTOR] Execution failed | Query: {sql_query} | Error: {str(e)}")
            return ErrorResponse(
                error="Invalid query. Please check your question and try again.",
                source="sql",
                details=str(e)
            )
            

        sql_query = sql_query.replace("```sql","").replace("```","").strip() 

        sql_query = sql_query.strip().rstrip(";")


        return SQLResponse(
            sql=sql_query,
            result=result
        )