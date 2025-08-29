from my_agents.myagent import myagent
from agents import Runner, set_tracing_disabled
import asyncio

set_tracing_disabled(True)

async def main():
        question = input("Hey!? ")
        response = await Runner.run(myagent,question)
        print(f"\n{response.final_output}")
asyncio.run(main())
