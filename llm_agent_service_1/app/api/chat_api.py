from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.agent.tool_agent import ToolAgent

router = APIRouter()

agent = ToolAgent()


@router.get("/chat")
def chat(query: str):

    result = agent.run(query)

    return {"result": result}


@router.get("/chat_stream")
async def chat_stream(query: str):

    async def generate():

        for chunk in agent.stream(query):

            yield chunk
            # 强制刷新缓冲区
            await asyncio.sleep(0)

    import asyncio

    return StreamingResponse(generate(), media_type="text/plain")