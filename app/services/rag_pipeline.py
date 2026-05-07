from app.services.retriever import Retriever
from app.schemas import QueryResponse
from app.chains.lcel_chain import LLMService


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.chain = LLMService()

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
        response = self.chain.generate(context, query)

        cleaned_answer = response.replace("\n", " ").replace("\\n", " ").strip()
        cleaned_docs = [" ".join(doc.replace("\n", " ").replace("\\n", " ").split()) for doc in docs]

        return {
            "answer": cleaned_answer,
            "context_docs": cleaned_docs
        }

        
