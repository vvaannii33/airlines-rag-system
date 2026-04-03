from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


class Retriever:
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize embeddings and vector DB
        """
        self.embedding = OpenAIEmbeddings()

        self.vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding
        )

    def get_relevant_docs(self, query: str, k: int = 3):
        """
        Retrieve top-k relevant documents
        """
        return self.vectordb.similarity_search(query, k=k)
