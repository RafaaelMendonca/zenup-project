from fastapi import APIRouter
from pydantic import BaseModel
from chatbot.chatbot import enviar_mensagem_async, gerar_resumo_async

router = APIRouter()

class ChatRequest(BaseModel):
    id: int
    texto: str | None = None
    resumo:str | None = None
    # encerramento: bool = False

@router.post("/chat")
async def chat_controller(req: ChatRequest):
    if req.texto:
        resposta = await enviar_mensagem_async(req.id, req.texto, req.resumo)
        return {"mensagem": resposta}
    return {"mensagem": "Nenhuma ação realizada"}

# criar uma de resumo
@router.get("/resumo/{id_usuario}")
async def gerar_resumo_controller(id_usuario:int):
    resumo = await gerar_resumo_async(id_usuario)
    return {"resumo": resumo}

# criar uma que vai receber a quantidade de dias em que o 