from langchain_core.prompts import ChatPromptTemplate
rag_prompt = ChatPromptTemplate.from_template("""
        Answer the question based on the context.
        If the context contains specific numerical information, use it to answer the question.
        If the answer contains context information as well as logical reasoning, separate them clearly in the answer.
        Do NOT display line breaks (\n) in the response. Use bullet points instead.
        Answer should be in a point-wise, structured and clear format.

        Context:
        {context}

        Question:
        {question}
        """)

