from fastapi import APIRouter, Request
from fastapi import UploadFile, File
import requests
import os

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


@router.post("/processar-pdf")
async def processar_pdf_endpoint(request: Request):
    files = await request.form()
    if "file" not in files:
        return {"erro": "Nenhum arquivo enviado"}
    
    file = files["file"]
    response = requests.post(
        "http://llm:5001/processar-pdf",
        files={"file": (file.filename, file.file, file.content_type)}
    )
    
    return response.json()
