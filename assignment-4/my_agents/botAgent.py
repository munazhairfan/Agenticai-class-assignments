from agents import Agent, GuardrailFunctionOutput, Runner,RunContextWrapper, ModelSettings, handoff, input_guardrail
from config.config import gemini_model
from data_classes.data_classes import NegativeSentiment, UserInfo
from my_agents.humanAgent import humanAgent
import logging
from fileReaders.filereaders import faqs
from tools.tools import get_order_status

# creating metadata
user1 = UserInfo(name="John",age="22")
user1_dict = {
    "name":user1.name,
    "age":user1.age
}

# checks if the user sentiment is offensive or negative
@input_guardrail
async def negative_sentiment(ctx:RunContextWrapper,agent:Agent,my_input:str):
    logging.info("Input guardrail triggered.")
    guardrail_agent = Agent(name="Guardrail agent",
                            instructions="Return True if the user uses offensive language otherwise False",
                            model=gemini_model,
                            output_type=NegativeSentiment)
    result = await Runner.run(starting_agent=guardrail_agent,input=my_input)

    if result.final_output.is_negative_word == True:
        logging.warning(f"Negative sentiment detected in user input.")
    else:
        logging.info("No offensive language or negative sentiment detected.")

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_negative_word,
    )

# runs when handoff occurs between botAgent and humanAgent
def handoff_function(ctx:RunContextWrapper):
    logging.info("Handoff to Human Agent occured.")


botAgent = Agent(name="Bot Agent",
                     instructions=f"""You are the Bot Agent. You only:  
                    - Answer FAQs: {faqs}.  
                    - Do not ask or inform the user before handing off
                    - Use get_order_status(order_id) for order queries.  
                    - Stay polite and clear.  
                    """,
                     tools = [get_order_status],
                     model_settings=ModelSettings(
                         tool_choice="auto",
                        #  metadata=user1_dict # Gemini’s compatibility layer does not implement this feature.
                         ),
                     input_guardrails=[negative_sentiment],
                     handoffs=[humanAgent],
                     handoff_description="""Handoff happens if:  
                    - Query is outside FAQs/order status, OR
                    - User is asking something that is not related to orders  
                    - Negative/offensive sentiment is detected.
                    """,
                     model=gemini_model)
human_agent_handoff = handoff(agent=humanAgent,tool_name_override="handed_over_to_human_agent",on_handoff=handoff_function)
