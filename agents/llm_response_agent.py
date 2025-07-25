import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMResponseAgent:
    def __init__(self, model="gpt-4"):
        self.model = model

    def generate_response(self, query, retrieved_chunks):
        context = "\n\n".join(retrieved_chunks)
        prompt = f"""You are a highly intelligent assistant that answers questions using only the provided document context.

Your goal is to answer the question as completely and accurately as possible, based only on this context.

If you truly cannot find an answer, say: "The answer is not available in the context."

---

Context:
{context}

---

Question: {query}
Answer:"""


        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a document-aware assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
