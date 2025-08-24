from agents import Agent
from config.config import gemini_model
from instructions.dynamic_instructions import my_agent_instructions

traige_agent = Agent(name="Choppy",instructions=my_agent_instructions,model=gemini_model)