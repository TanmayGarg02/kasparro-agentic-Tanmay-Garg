from fastapi import FastAPI
from pydantic import BaseModel
from agents.faq_agent import faq_agent
import uvicorn

app = FastAPI(title="Agentic AI System")

class UserQuery(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(payload: UserQuery):
    response = faq_agent.run(payload.question)
    return {"answer": response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
