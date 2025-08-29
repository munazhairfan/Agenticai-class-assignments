from agents import Agent
from config.config import gemini_model
from tools.tool import webSearchtool


myagent = Agent(name="Choppy",
                     instructions="You are a helpful chatbot",
                     model=gemini_model,
                     tools=[webSearchtool],
                     )
