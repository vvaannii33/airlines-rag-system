from app.services.sql_chain import SQLChain
from app.services.rag_pipeline import RAGPipeline
from app.services.router import QueryRouter


class HybridPipeline:
    def __init__(self):
        self.sql_chain = SQLChain()
        self.rag = RAGPipeline()
        self.router = QueryRouter()

    def split_query(self, question:str):
        question_lower = question.lower()

        split_keywords = ["and","also",",","then","+","as well as","followed by"]

        for keyword in split_keywords:
            if keyword in question_lower:
                parts = question_lower.split(" and ",1)
                return parts[0].strip(), parts[1].strip()
        return question, None

    def run(self, question: str):

        route = self.router.route(question)

        if route == "mixed":
            sql_part, rag_part = self.split_query(question)

            sql_result = self.sql_chain.run(sql_part)
            rag_result = self.rag.run(rag_part)

            return {
                "source" : "mixed",
                "sql" : sql_result,
                "rag" : rag_result
            }

        elif route == "sql":
            return {
                "source" : "sql",
                "response" : self.sql_chain.run(question)
            }

        else:
            return {
                "source" : "rag",
                "response" : self.rag.run(question)
            }

