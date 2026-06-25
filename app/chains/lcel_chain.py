from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from app.prompts.rag_prompt import rag_prompt
import uuid


class LLMService:
    def __init__(self):
        

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )

        request_id = str(uuid.uuid4())[:8]

        self.parser = StrOutputParser()

        self.prompt = rag_prompt

        self.chain = self.prompt | self.llm | self.parser

    def generate(self, context, question, request_id):
        return self.chain.invoke({
            "context": context,
            "question": question,
            "request_id": request_id
        })