from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health_check():
    """Check if the service is running"""
    return {"status": "healthy"}
