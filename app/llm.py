from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


class LLMHandler:
    def __init__(self):
        """
        Initialize LLM
        """
        self.llm = ChatOpenAI(temperature=0)

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are an airline assistant.

Use the following context to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def generate_response(self, context: str, question: str):
        """
        Generate answer from LLM
        """
        prompt = self.prompt.format(context=context, question=question)
        return self.llm.predict(prompt)
