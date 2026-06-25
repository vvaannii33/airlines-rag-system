from app.utils.logger_config import logger

class QueryRouter:
    def route(self, question: str) -> str:
        question_lower = question.lower()

        sql_keywords = [
            "flight", "passenger", "booking",
            "show", "list", "count", "how many",
            "after", "before", "between"
        ]

        rag_keywords = [
            "what is", "define",
            "explain", "describe", "tell me about"
        ]

        is_rag = any(k in question_lower for k in rag_keywords)

        is_sql = any(k in question_lower for k in sql_keywords)

        if is_rag and is_sql:
            logger.info(f"[QUERY_ROUTER] Mixed query detected. Routing to hybrid pipeline.")
            return "mixed"
        elif is_sql:
            route_chosen = "sql"
            logger.info(f"[QUERY_ROUTER] SQL query detected.")
            logger.info(f"[QUERY_ROUTER] Route chosen: {route_chosen}")
            return "sql"
        else:
            route_chosen = "rag"
            logger.info(f"[QUERY_ROUTER] RAG query detected.")
            logger.info(f"[QUERY_ROUTER] Route chosen: {route_chosen}")
            return "rag"