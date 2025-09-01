from guardrails.inputGuardrail import indian_queries_input_guardrail
from guardrails.outputGuardrail import US_queries_output_guardrail
from agents import Agent, function_tool


@function_tool
def find_hotels(city: str, date: str) -> str:
    return f"""hotel available on {date} in {city} are following
    - PC Hotel, 1 Night stay rent is 15000, Breakfast included, free parking
    - Marriott, 1 Night stay rent is 13000, Breakfast included, free parking
    - Movenpick, 1 Night stay rent is 14000, Breakfast included, free wifi
    """


hotel_agent = Agent(
    name="HotelAgent",
    instructions="You are a hotel agent. Find best and cheap hotel in provided city",
    handoff_description="find hotels in city",
    tools=[find_hotels],
    input_guardrails=[indian_queries_input_guardrail],
    output_guardrails=[US_queries_output_guardrail]
)
