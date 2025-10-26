from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI(title="Service A")

# Используйте имя сервиса из docker-compose вместо 0.0.0.0
SERVICE_B_URL = os.getenv("SERVICE_B_URL", "http://service_b:8001")

@app.get("/")
async def root():
    return {"message": "Hello from Service A!"}

@app.get("/process-data")
async def process_data():
    """Обрабатывает данные и передает в Service B"""
    data = {
        "service": "A",
        "action": "process",
        "data": {"numbers": [1, 2, 3, 4, 5], "message": "Hello from Service A"}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SERVICE_B_URL}/receive-data", 
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return {
                "status": "success", 
                "processed_by": "Service A",
                "response_from_b": result
            }
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with Service B: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "A"}