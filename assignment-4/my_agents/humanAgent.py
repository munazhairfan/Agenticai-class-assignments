from agents import Agent
from config.config import gemini_model

# answers when the query is too complex or negative
humanAgent = Agent(name="Human Agent",
                     instructions="""You are the Human Agent.  
                    - Step in only when handed off.  
                    - Handle complex, unclear, or negative queries. 
                    - Handle questions unrelated to orders 
                    - Be empathetic and professional.
                    """,
                    #  input_guardrails=[negative_sentiment],
                     model=gemini_model)
