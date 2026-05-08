import sqlparse

class SQLValidator:
    def validate_sql(self, sql_query: str, user_role: str = "user"):
        try:
            parsed = sqlparse.parse(sql_query)
        
        

            if not parsed:
                return False, "Invalid SQL"

            for stmt in parsed:
                #Detect query type (SELECT / INSERT / etc)
                first_token = None
                for token in stmt.tokens:
                    if not token.is_whitespace:
                        first_token = token
                        break

                if first_token is None:
                    return False, "Empty query"

                query_type = first_token.value.upper()

                #Block non-read queries for non-admin
                if user_role != "admin":
                    if query_type not in ["SELECT", "WITH", "EXPLAIN"]:
                        return False, f"{query_type} not allowed"

                #Block destructive keywords even if hidden
                blocked_operations = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE"]

                for token in stmt.tokens:
                    token_value = str(token.value).upper().strip()
                    if any(op in token_value for op in blocked_operations):
                        if user_role != "admin":
                            return False, f"{token_value} operation not allowed"

            return True, "Safe"

        except Exception as e:
            logger.error(f"Execution Error: {str(e)}")
            return False, f"Parsing error: {str(e)}"
            