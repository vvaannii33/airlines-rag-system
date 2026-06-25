from dotenv import load_dotenv
load_dotenv()
from langchain_chroma import Chroma
from app.exceptions.custom_exceptions import RetrievalError
from app.utils.logger_config import logger
from langchain_openai import OpenAIEmbeddings
from app.utils.constants import CHROMA_DB_DIR

class Retriever:
    def __init__(self):

        self.embedding = OpenAIEmbeddings()
        # Create vector DB
        self.vectorstore = Chroma(
            persist_directory=str(CHROMA_DB_DIR),
            embedding_function=self.embedding,
            collection_name="airlines_rag"
        )

        count = self.vectorstore._collection.count()
        logger.info(f"[RETRIEVER] Initialized with {count} documents")

    def get_relevant_docs(self, query):
        try:
            results = self.vectorstore.similarity_search_with_relevance_scores(query, k=3)
            relevant_docs = []
            seen = set()
            for doc, relevance_score in results:

                    print("=" * 50)
                    print(doc.page_content)
                    print()
                    print("Question:",query)
                    print("Relevance Score:", relevance_score)
            logger.info(f"[RETRIEVER] Retrieved {len(results)} documents for query: {query}")
            return [doc for doc,relevance_score in results]

        
        except Exception as e:
            logger.error(f"[RETRIEVER] Error retrieving documents for query: {query} | Error: {str(e)}")
            raise RetrievalError(f"Error retrieving documents: {str(e)}")

#ensures the test code only runs when you directly execute the file
if __name__ == "__main__":
    retriever = Retriever()        # Create the object
    print("Retriever initialized successfully!")
        
