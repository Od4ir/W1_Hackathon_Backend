from fastapi import APIRouter, Request
import requests

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello from W1 Hackathon Backend 💖"}

@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    mensagem = data.get("mensagem")
    if not mensagem:
        return {"erro": "Mensagem não fornecida"}
    response = requests.post("http://llm:5001/mensagem", json={"mensagem": mensagem})
    return {"resposta": response.json().get("resposta")}

