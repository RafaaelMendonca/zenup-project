from fastapi import APIRouter
from pydantic import BaseModel
from chatbot.chatbot import enviar_mensagem_async, gerar_resumo_async

router = APIRouter()

class ChatRequest(BaseModel):
    id: int
    texto: str | None = None
    encerramento: bool = False

@router.post("/chatbot")
async def chat_controller(req: ChatRequest):
    if req.encerramento and req.texto:
        await enviar_mensagem_async(req.id, req.texto)

    if req.encerramento:
        resumo = await gerar_resumo_async(req.id)
        return {"resumo": resumo}

    if req.texto:
        resposta = await enviar_mensagem_async(req.id, req.texto)
        return {"mensagem": resposta}

    return {"msg": "Nenhuma conversa para processar."}
