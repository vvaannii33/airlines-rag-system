# app/llm.py

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),timeout=10)


class LLMService:
    def generate_response(self, context: str, query: str) -> str:
        try:
            prompt = f"""
            You are an expert assistant for answering questions based on documents.

            STRICT RULES:
            1. Answer ONLY from the given context
            2. Do NOT make up information
            3. If unsure, say "I don't know"
            4. Keep answers clear and concise

            Context:
            {context}

            User Question:
            {query}

            Final Answer:
            """

            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

            return response.choices[0].message.content or "I don't know"

        except Exception as e:
            return "Error generating response"