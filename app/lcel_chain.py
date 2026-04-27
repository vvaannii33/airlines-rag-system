from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class LCELChain:

    def __init__(self):
        
        self.prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the context below.
        If the answer is not in the context, say "I don't know".

        Context:
        {context}

        Question:
        {question}
        """
        )

        self.llm = ChatOpenAI(model="gpt-4o-mini")

        self.parser = StrOutputParser()

        self.chain = self.prompt | self.llm | self.parser

    def run(self,context,question):
        return self.chain.invoke({
         "context": context,
         "question": question
        })