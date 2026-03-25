import app.skills
from app.agent.tool_agent import ToolAgent

class AgentService:

    def __init__(self):
        self.agent = ToolAgent()

    def run(self, query: str):

        print("用户:", query)

        return self.agent.run(query)