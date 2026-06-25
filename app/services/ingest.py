# Load environment variables from .env file
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# Chroma vector database
from langchain_chroma import Chroma

# OpenAI embedding model
from langchain_openai import OpenAIEmbeddings

# Text splitter used for chunking large documents
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Project constant containing chroma_db path
from app.utils.constants import CHROMA_DB_DIR

# PDF loader used to read PDF files
from langchain_community.document_loaders import PyPDFLoader

from app.utils.logger_config import logger


class Ingest:

    def __init__(self):

        # Path of the PDF file to ingest
        pdf_path = "Dataset - Flykite Airlines_HRP.pdf"

        # Create PDF loader object
        loader = PyPDFLoader(pdf_path)

        # Load all PDF pages as LangChain Documents
        documents = loader.load()

        # Display number of pages loaded
        print(f"Total pages loaded: {len(documents)}")

        # Create embedding model object
        self.embedding = OpenAIEmbeddings()

        # Configure chunking strategy
        self.splitter = RecursiveCharacterTextSplitter(

            # Maximum characters per chunk
            chunk_size=500,

            # Overlap helps preserve context between chunks
            chunk_overlap=100
        )

        # Split PDF pages into smaller chunks
        self.docs = self.splitter.split_documents(documents)

        # Display number of chunks generated
        print(f"Chunks created: {len(self.docs)}")

        existing_db = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=self.embedding,
        collection_name="airlines_rag"
        )

        try:
            existing_db.delete_collection()
            logger.info("Existing collection deleted.")
        except Exception as e:
            logger.warning("Collection does not exist.")
            print("Collection does not exist.")

        # Create vector database from document chunks
        self.vectorstore = Chroma.from_documents(

            # Chunks to store
            documents=self.docs,

            # Embedding model used to vectorize chunks
            embedding=self.embedding,

            # Folder where vectors will be persisted
            persist_directory=str(CHROMA_DB_DIR),

            # Collection name inside Chroma
            collection_name="airlines_rag"
        )

        # Display number of vectors stored
        count = self.vectorstore._collection.count()
        logger.info(f"[INGEST] Ingested {count} chunks into vector store")


# Entry point
if __name__ == "__main__":

    # Run ingestion process
    Ingest()

    print("Ingestion completed.")