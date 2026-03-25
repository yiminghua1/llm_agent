from openai import OpenAI
from app.config import LLM_BASE_URL, LLM_API_KEY

class LLMClient:

    def __init__(self):

        self.client = OpenAI(
            base_url=LLM_BASE_URL,
            api_key=LLM_API_KEY
        )