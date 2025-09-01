from typing import Literal
from agents import (
    Agent,
    HandoffInputData,
    RunContextWrapper,
    Runner,
    RunConfig,
    TResponseInputItem,
    handoff,
    set_tracing_disabled,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
    
)
from pydantic import BaseModel
from guardrails.inputGuardrail import indian_queries_input_guardrail
from guardrails.outputGuardrail import US_queries_output_guardrail

from my_agents.weather_agent import weather_agent
from my_agents.hotel_agent import hotel_agent
from my_agents.flight_agent import flight_agent
from config.config import gemini_model
from agents.extensions import handoff_filters

import asyncio

set_tracing_disabled(True)

class Users(BaseModel):
    name: str
    role: Literal["admin", "super user", "basic"]
    age: int


# user = Users(name="abc", role="admin", age=20)
async def handoff_permission(ctx: RunContextWrapper[Users], agent: Agent) -> bool:
    if ctx.context.age > 25:
        return True

    if ctx.context.role == "super user":
        return True
    return False


def handoff_filter(data: HandoffInputData) -> HandoffInputData:
    data = handoff_filters.remove_all_tools(data)
    history = data.input_history[-2:]

    return HandoffInputData(
        input_history=history,
        new_items=data.new_items,
        pre_handoff_items=data.pre_handoff_items,
    )


triage_agent = Agent(
    name="TriageAgent",
    instructions="""
    you are a triage agent, hand off to flight,hotel or weather agent 
    if user ask for otherwise you can response yourself
    """,
    handoffs=[
        handoff(
            agent=weather_agent,
            tool_name_override="handoff_weatheragent",
            tool_description_override="handoff to weather agent to get the weather information",
            is_enabled=handoff_permission,
            input_filter=handoff_filter,
        ),
        hotel_agent,
        flight_agent,
    ],
    handoff_description="""
    this triage agent, hand off to flight,hotel or weather agent 
    if user ask for otherwise you can response yourself""",
)

weather_agent.handoffs.append(triage_agent)
hotel_agent.handoffs.append(triage_agent)
flight_agent.handoffs.append(triage_agent)

try:
    async def main():
        user = Users(name="abc", role="super user", age=20)
        start_agent = triage_agent
        input_data: list[TResponseInputItem] = []
        while True:
            user_prompt = input("enter your query : ")
            if user_prompt == "exit":
                break

            input_data.append({"role": "user", "content": user_prompt})

            result = await Runner.run(
                start_agent,
                input=input_data,
                run_config=RunConfig(
                    model=gemini_model, 
                    tracing_disabled=False,
                    input_guardrails=[indian_queries_input_guardrail],
                    output_guardrails=[US_queries_output_guardrail]),
                context=user,
            )
            start_agent = result.last_agent
            input_data = result.to_input_list()

            print(result.final_output)
    asyncio.run(main())
except (InputGuardrailTripwireTriggered):
    print("Sorry! I can't provide any information about India.")
except (OutputGuardrailTripwireTriggered):
    print("Sorry! I can't provide any information about US.")
    
