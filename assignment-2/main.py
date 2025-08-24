from typing import Any
from openai import AsyncOpenAI
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    OpenAIChatCompletionsModel,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    InputGuardrailTripwireTriggered,
    set_tracing_disabled
)
from dotenv import find_dotenv, load_dotenv
import os
import asyncio

from pydantic import BaseModel

load_dotenv(find_dotenv(), override=True)
set_tracing_disabled(True)

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("GEMINI_MODEL_NAME")


client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model=model_name,openai_client=client)


class MathOutPut(BaseModel):
    is_math: bool
    reason: str

class PoliticalOutput(BaseModel):
    is_political : bool

@input_guardrail
async def check_input(
    ctx: RunContextWrapper[Any], agent: Agent[Any], input_data: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:

    input_agent = Agent(
        "InputGuardrailAgent",
        instructions="Check and verify if input is related to math",
        model=model,
        output_type=MathOutPut,
    )
    result = await Runner.run(input_agent, input_data, context=ctx.context)
    final_output = result.final_output

    return GuardrailFunctionOutput(
        output_info=final_output, tripwire_triggered=final_output.is_math
    )

@output_guardrail
async def check_output(
    ctx: RunContextWrapper[Any], agent: Agent[Any], output_data: Any
) -> GuardrailFunctionOutput:

    output_agent = Agent(
        "OutputGuardrailAgent",
        instructions="Check and verify if output contains any political topics and references to political figures." \
        "and if it does then return True",
        model=model,
        output_type=PoliticalOutput,
    )
    result = await Runner.run(output_agent, output_data, context=ctx.context)
    final_output = result.final_output

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=final_output.is_political
    )


# math_agent = Agent(
#     "MathAgent",
#     instructions="You are a math agent",
#     model=model,
#     input_guardrails=[check_input],
#     # input_guardrails=[InputGuardrail(guardrail_function=check_input)]
# )

general_agent = Agent(
    "GeneralAgent",
    instructions="You are a helpful agent",
    model=model,
    input_guardrails=[check_input],
    output_guardrails=[check_output],
)


async def main():
    try:
        msg = input("Enter you question : ")
        result = await Runner.run(general_agent, msg)
        print(f"\n\n final output : {result.final_output}")
    except (InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered) as ex:
        print("Error : invalid prompt")


asyncio.run(main())