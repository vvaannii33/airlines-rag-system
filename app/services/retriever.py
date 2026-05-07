from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Retriever:
    def __init__(self):
        self.embedding = OpenAIEmbeddings()

        # Original documents (simulate real data)
        self.raw_docs = [
            """Probation is a trial period before full employment.
            It helps evaluate employee performance and cultural fit.
            Typically lasts 3 to 6 months depending on company policy.""",

            """UNICEF stands for United Nations International Children's Emergency Fund.
            It works globally to provide humanitarian aid to children.""",

            """Large Language Models (LLMs) are AI systems trained on vast amounts of text data.
            They are used for tasks like question answering, summarization, and chatbots."""
        ]

        # 🔥 Chunking step
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,       # small for demo (increase later)
            chunk_overlap=40
        )

        self.docs = self.splitter.create_documents(self.raw_docs)

        # Create vector DB
        self.vectorstore = Chroma.from_documents(
            documents=self.docs,
            embedding=self.embedding
        )

    def get_relevant_docs(self, query):
        results = self.vectorstore.similarity_search(query, k=2)
        return [doc.page_content for doc in results]
