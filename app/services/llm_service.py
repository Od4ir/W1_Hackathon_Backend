import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")

async def get_llm_response(prompt: str) -> str:
    # Exemplo fictício de chamada
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.generative.google.com/v1/fake_endpoint",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"prompt": prompt}
        )
        return response.json().get("response", "Sem resposta 😵‍💫")
