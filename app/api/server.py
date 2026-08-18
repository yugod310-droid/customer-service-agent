from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.customer_agent import handle_customer_query

app = FastAPI(title="Customer Service Agent API", version="0.1.0")


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "customer-service-agent"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    result = handle_customer_query(request.message or "")
    return result
