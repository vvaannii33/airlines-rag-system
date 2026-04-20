from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def build_chain():
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the context below.
        If the answer is not in the context, say "I don't know".

        Context:
        {context}

        Question:
        {question}
        """
    )

    llm = ChatOpenAI(model="gpt-4o-mini")

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return chain
