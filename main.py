from fastapi import FastAPI
from controllers.chatbot_controller import router as chat_router

app = FastAPI()

app.include_router(chat_router, prefix="/api", tags=["Zen_API"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
