from agents import Agent, function_tool
from guardrails.inputGuardrail import indian_queries_input_guardrail
from guardrails.outputGuardrail import US_queries_output_guardrail

@function_tool
def find_flights(from_city: str, to_city: str, date: str) -> str:
    return f"""flight PK100 available from {from_city} to {to_city} on {date}
    price are 28000 PKR
    """


flight_agent = Agent(
    name="FlightAgent",
    instructions="You are a flight agent. Find best and cheap flights between two cities",
    handoff_description="find best flights between two cities",
    tools=[find_flights],
    input_guardrails=[indian_queries_input_guardrail],
    output_guardrails=[US_queries_output_guardrail]
)