# app/llm.py

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class LLMService:
    def generate_response(self, context: str, query: str) -> str:
        """
        Generates answer using OpenAI
        """

        prompt = f"""
        You are a helpful assistant.

        Use the context below to answer the question.
        If answer is not in context, say "I don't know".

        Context:
        {context}

        Question:
        {query}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content