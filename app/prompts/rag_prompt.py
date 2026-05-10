from langchain.prompts import ChatPromptTemplate
rag_prompt = ChatPromptTemplate.from_template("""
        Answer the question based only on the context below.
        If the question is out of context, say "Invalid question".
        Do NOT display line breaks (\n) in the response. Use bullet points instead.
        Answer should be in a point-wise, structured and clear format.

        Context:
        {context}

        Question:
        {question}
        """)

