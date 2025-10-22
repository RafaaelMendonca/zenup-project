from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import secrets

from chatbot.chatbot import (
    enviar_mensagem_async,
    gerar_resumo_async,
    enviar_mensagem_proativa_async,
)

load_dotenv()
CHAVE_SECRETA = os.getenv("API_SECRET_KEY")
if not CHAVE_SECRETA:
    raise RuntimeError("API_SECRET_KEY não encontrada no .env")

usuarios_ativos = {}

router = APIRouter()


class LoginRequest(BaseModel):
    chave: str


@router.post("/login")
async def login(req: LoginRequest):
    if req.chave != CHAVE_SECRETA:
        raise HTTPException(status_code=401, detail="Chave inválida")

    token = secrets.token_hex(16)
    usuarios_ativos[token] = {"ativo": True}
    return {"token": token}

async def verificar_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    token = authorization.replace("Bearer ", "")
    if token not in usuarios_ativos or not usuarios_ativos[token]["ativo"]:
        raise HTTPException(status_code=401, detail="Token inválido ou não autorizado")

    return token

class ChatRequest(BaseModel):
    id: int
    texto: Optional[str] = None
    resumo: Optional[str] = None


@router.post("/chat")
async def chat_controller(req: ChatRequest, token: str = Depends(verificar_token)):
    if not req.texto or not req.texto.strip():
        raise HTTPException(status_code=422, detail="Texto não pode estar vazio")

    resposta = await enviar_mensagem_async(req.id, req.texto, req.resumo)
    return {"mensagem": resposta}


@router.get("/resumo/{id_usuario}")
async def gerar_resumo_controller(id_usuario: int, token: str = Depends(verificar_token)):
    resumo = await gerar_resumo_async(id_usuario)
    return {"resumo": resumo}


@router.get("/ia_proativa/{id_usuario}")
async def ia_proativa_controller(id_usuario: int, token: str = Depends(verificar_token)):
    resposta = await enviar_mensagem_proativa_async(id_usuario)
    return {"mensagem": resposta}
