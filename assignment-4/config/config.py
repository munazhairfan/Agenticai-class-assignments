import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=client)
