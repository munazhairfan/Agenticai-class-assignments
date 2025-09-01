from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, input_guardrail
from pydantic import BaseModel
from config.config import gemini_model

class indian_query(BaseModel):
    is_query_about_indian_city:bool
@input_guardrail
async def indian_queries_input_guardrail(ctx:RunContextWrapper,agent:Agent,my_input:str):
    guardrail_agent = Agent(name="Input Guardrail Agent",
                            instructions="Return True if the user's query is related to India, Indian region, Indian area or Indian cities otherwise False",
                            output_type=indian_query,
                            model=gemini_model)
    result = await Runner.run(starting_agent=guardrail_agent,input=my_input)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_query_about_indian_city,
    )