from my_agents.my_agent import traige_agent
from agents import Runner, set_tracing_disabled
from my_dataclasses.my_dataclasses import user

set_tracing_disabled(True)

question = input("Hey! How can I help you today? ")
response = Runner.run_sync(traige_agent,question,context=user)
print(f"\n{response.final_output}")