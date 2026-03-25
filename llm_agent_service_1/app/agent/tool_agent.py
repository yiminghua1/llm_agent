import json
import time
from pathlib import Path

from app.llm.client import LLMClient
from app.agent.tool_builder import build_tools
from app.skills.skill_registry import get_skill
from app.config import LLM_MODEL


class ToolAgent:

    def __init__(self):

        self.llm = LLMClient()

        # ======================
        # 加载城市映射
        # ======================

        city_path = Path(__file__).resolve().parent.parent / "city_map.json"

        with open(city_path, "r", encoding="utf-8") as f:
            self.city_map = json.load(f)

        print("城市映射加载:", self.city_map)

    # ======================
    # 城市识别
    # ======================

    def detect_city(self, query):

        city = "wuhan"

        for k, v in self.city_map.items():
            if k in query:
                city = v
                break

        return city

    # ======================
    # 主 Agent 逻辑
    # ======================

    def run(self, query):

        tools = build_tools()

        messages = [
            {
                "role": "system",
                "content": """
你是一个智能助手。

你可以使用以下工具：

weather(city) 查询城市天气
time() 查询当前时间

如果用户询问天气或时间，请优先调用工具，而不是自己编造答案。
"""
            },
            {
                "role": "user",
                "content": query
            }
        ]

        # ======================
        # 第一次调用 LLM
        # ======================

        response = self.llm.client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        print("LLM响应:", response)

        tool_calls = message.tool_calls or []

        # ======================
        # fallback reasoning
        # ======================

        if not tool_calls and hasattr(message, "reasoning"):

            reasoning = message.reasoning.lower()

            print("reasoning:", reasoning)

            tool_calls = []

            if "weather" in reasoning:

                city = self.detect_city(query)

                tool_calls.append({
                    "name": "weather",
                    "arguments": json.dumps({"city": city})
                })

            if "time" in reasoning:

                tool_calls.append({
                    "name": "time",
                    "arguments": "{}"
                })

        # ======================
        # 没有工具调用
        # ======================

        if not tool_calls:

            return message.content or "我暂时无法回答这个问题"

        # ======================
        # 执行工具
        # ======================

        tool_results = []

        for tool_call in tool_calls:

            if isinstance(tool_call, dict):

                name = tool_call["name"]
                args = json.loads(tool_call["arguments"])

            else:

                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

            print("调用工具:", name, args)

            skill = get_skill(name)

            if not skill:
                continue

            result = skill["instance"].run(**args)

            tool_results.append(f"{name}结果: {result}")

        context = "\n".join(tool_results)

        print("工具返回:", context)

        # ======================
        # 第二次调用 LLM
        # ======================

        final = self.llm.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""
你是一个智能助手。

以下是工具返回数据：

{context}

请根据这些数据回答用户问题。
"""
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        return final.choices[0].message.content

    # ======================
    # Streaming
    # ======================

    def stream(self, query):

        # 先运行完整 Agent
        result = self.run(query)

        if not result:
            result = "我暂时无法回答这个问题"

        buffer = ""

        for ch in result:

            buffer += ch

            # 每5个字符返回一次
            if len(buffer) >= 5:

                yield buffer
                buffer = ""

                time.sleep(0.02)

        if buffer:
            yield buffer