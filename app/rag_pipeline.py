from app.retriever import Retriever
from app.schemas import QueryResponse
from app.lcel_chain import LCELChain


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.chain = LCELChain()

    def run(self, query: str):
        """
        Full RAG pipeline:
        1. Retrieve docs
        2. Build context
        3. Generate answer
        """

        #retrieve relevant docs based on query
        docs = self.retriever.get_relevant_docs(query)

        #convert docs to context string for LLM input
        context = "\n\n".join(f"Document {i+1} : {doc}" for i,doc in enumerate(docs))

        #LCEL call to generate answer
        response = self.chain.run(context, query)

        #return answer and source docs
        return {
        "answer": response,
        "context_docs": docs
        }
