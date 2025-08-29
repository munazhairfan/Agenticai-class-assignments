import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from tavily import TavilyClient

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=tavily_key)
client = AsyncOpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=client)
