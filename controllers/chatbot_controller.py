from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chatbot.chatbot import enviar_mensagem_async, gerar_resumo_async, enviar_mensagem_proativa_async

router = APIRouter()


class ChatRequest(BaseModel):
    id: int
    texto: Optional[str] = None
    resumo: Optional[str] = None


@router.post("/chat")
async def chat_controller(req: ChatRequest):
    """
    Recebe uma mensagem do usuário e retorna a resposta do chatbot.
    """
    if not req.texto or not req.texto.strip():
        raise HTTPException(status_code=422, detail="Texto não pode estar vazio")

    resposta = await enviar_mensagem_async(req.id, req.texto, req.resumo)
    return {"mensagem": resposta}


@router.get("/resumo/{id_usuario}")
async def gerar_resumo_controller(id_usuario: int):
    """
    Gera e retorna um resumo da conversa do usuário.
    """
    resumo = await gerar_resumo_async(id_usuario)
    return {"resumo": resumo}


@router.get("/ia_proativa/{id_usuario}")
async def ia_proativa_controller(id_usuario: int):
    """
    Retorna uma mensagem proativa da IA quando o usuário está em estado emocional crítico.
    """
    resposta = await enviar_mensagem_proativa_async(id_usuario)
    return {"mensagem": resposta}
