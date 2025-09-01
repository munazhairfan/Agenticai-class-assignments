from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, output_guardrail
from pydantic import BaseModel
from config.config import gemini_model

class US_query(BaseModel):
    is_query_about_us_city:bool
@output_guardrail
async def US_queries_output_guardrail(ctx:RunContextWrapper,agent:Agent,output_data:any):
    guardrail_agent = Agent(name="Input Guardrail Agent",
                            instructions="Return True if the assistants's response is related to United States, United States region, United States area or United States cities otherwise False",
                            output_type=US_query,
                            model=gemini_model)
    result = await Runner.run(starting_agent=guardrail_agent,input=output_data,context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_query_about_us_city,
    )   