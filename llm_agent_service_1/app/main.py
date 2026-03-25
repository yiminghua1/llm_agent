from fastapi import FastAPI
from app.services.agent_service import AgentService
from app.api.chat_api import router

app = FastAPI()
app.include_router(router)
agent = AgentService()

# @app.get("/chat")
# def chat(query: str):
#     result = agent.run(query)
#     return {"result": result}