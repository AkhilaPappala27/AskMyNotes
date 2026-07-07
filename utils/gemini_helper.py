import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_answer(question, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful AI study assistant.

Answer the user's question ONLY using the provided context.
If the answer is not present in the context, reply:
"I couldn't find the answer in the uploaded study materials."

Context:
{context}

Question:
{question}

Answer:
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text