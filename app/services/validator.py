import sqlparse
from app.utils.logger_config import logger
from app.exceptions.custom_exceptions import ValidationError

class SQLValidator:
    def validate_sql(self, sql_query: str, user_role: str = "user"):
        try:
            parsed = sqlparse.parse(sql_query)
            logger.info("[VALIDATOR] SQL Query parsed successfully")
        

            if not parsed:
                logger.error(f"[VALIDATOR] SQL parsing error: {str(e)}")
                raise ValidationError("Invalid SQL query")

            for stmt in parsed:
                #Detect query type (SELECT / INSERT / etc)
                first_token = None
                for token in stmt.tokens:
                    if not token.is_whitespace:
                        first_token = token
                        break

                if first_token is None:
                    raise ValidationError("Empty SQL query")

                query_type = first_token.value.upper()

                #Block non-read queries for non-admin
                if user_role != "admin":
                    if query_type not in ["SELECT", "WITH", "EXPLAIN"]:
                        raise ValidationError(f"{query_type} not allowed")

                #Block destructive keywords even if hidden
                blocked_operations = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE"]

                for token in stmt.tokens:
                    token_value = str(token.value).upper().strip()
                    if any(op in token_value for op in blocked_operations):
                        if user_role != "admin":
                            logger.warning(f"[VALIDATOR] Blocked operation detected: {token_value}")
                            raise ValidationError(f"{token_value} operation not allowed")

            return True, "Safe"

        except Exception as e:
            logger.error(f"[VALIDATOR] Execution Error: {str(e)}")
            raise ValidationError(f"Parsing error: {str(e)}")