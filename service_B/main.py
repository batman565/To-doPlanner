from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="Service B")

class DataFromA(BaseModel):
    service: str
    action: str
    data: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "Hello from Service B!"}

@app.post("/receive-data")
async def receive_data(data: DataFromA):
    """Получает данные от Service A и обрабатывает их"""
    processed_data = {
        "received_from": data.service,
        "processed_by": "Service B",
        "original_data": data.data,
        "computation": {
            "sum_of_numbers": sum(data.data.get("numbers", [])),
            "message_length": len(data.data.get("message", "")),
            "processed_at": "Service B"
        }
    }
    
    return {
        "status": "data received and processed",
        "processed_data": processed_data
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "B"}