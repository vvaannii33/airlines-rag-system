from app.retriever import Retriever
from app.llm import LLMHandler


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMHandler()

    def run(self, query: str):
        """
        Full RAG pipeline:
        1. Retrieve docs
        2. Build context
        3. Generate answer
        """

        docs = self.retriever.get_relevant_docs(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        response = self.llm.generate_response(context, query)

        return {
            "answer": response,
            "context_docs": docs
        }
