from fastapi import FastAPI
from src.app.chat.router import router as chat_router

app = FastAPI()

@app.get("/health")
async def health_check():
    """Check if the service is running"""
    return {"status": "healthy"}


app.include_router(chat_router)
