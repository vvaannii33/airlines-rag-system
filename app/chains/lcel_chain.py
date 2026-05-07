from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class LLMService:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        Answer the question based only on the context below.
        If the answer is not in the context, say "I don't know".
        Do NOT display line breaks (\n) in the response. Use bullet points instead.
        Answer should be in a point-wise, structured and clear format.

        Context:
        {context}

        Question:
        {question}
        """)

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )

        self.parser = StrOutputParser()

        self.chain = self.prompt | self.llm | self.parser

    def generate(self, context, question):
        return self.chain.invoke({
            "context": context,
            "question": question
        })
