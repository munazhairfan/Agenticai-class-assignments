from my_agents.botAgent import botAgent
from agents import Runner, set_tracing_disabled
import asyncio
import logging

set_tracing_disabled(True)

# Configure logging once at the start
logging.basicConfig(
    level=logging.INFO,  # INFO = normal logs, DEBUG = detailed
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot_agent.log"),  # write logs to a file
        logging.StreamHandler()                # also print to console
    ]
)

try:    
    async def main():
        logging.info("Starting system...")
        question = input("Hey! How can I help you today? ")
        response = await Runner.run(botAgent,question,context={"input":question})
        print(f"\n{response.final_output}")
    asyncio.run(main())
except Exception:
    logging.warning("Tripewire Triggered.")
    print("Please keep the conversation respectful so I can assist you better.")
