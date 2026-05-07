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
            return "mixed"
        elif is_sql:
            return "sql"
        else:
            return "rag"