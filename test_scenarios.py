from dotenv import load_dotenv
load_dotenv()
from app.services.retriever import Retriever

retriever = Retriever()

docs = retriever.get_relevant_docs(
    "What is probation?"
)

for doc in docs:
    print(doc.page_content)