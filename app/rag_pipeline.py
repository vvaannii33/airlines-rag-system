from app.retriever import Retriever
from app.llm import LLMService
from app.schemas import QueryResponse


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()

    def run(self, query: str):
        """
        Full RAG pipeline:
        1. Retrieve docs
        2. Build context
        3. Generate answer
        """

        #docs = self.retriever.get_relevant_docs(query)

        docs = ["UNICEF stands for the United Nations International Children's Emergency Fund",
        "Probation is a trail process before full employment. It was created to evaluate the employee's performance and fit within the company culture. The duration of probation can vary but typically lasts between 3 to 6 months. During this period, employees may receive additional training and support to help them succeed in their role. At the end of the probation period, a performance review is conducted to determine if the employee will be offered a permanent position or if their employment will be terminated."] 

        context = "\n\n".join(docs)

        response = self.llm.generate_response(context, query)

        return {
    "answer": response,
    "context_docs": docs
}
