from agents import RunContextWrapper, Agent
from my_dataclasses.my_dataclasses import User_info, floe,moon,royal,ballerina,Jasmine

def my_agent_instructions(ctx:RunContextWrapper[User_info],agent:Agent[User_info]):
    hotels = [floe, moon, royal, ballerina, Jasmine]
    hotels_str = "\n".join([f"- {h.name} in {h.location}, {h.rooms} rooms, "
                            f"Amenities: {', '.join(h.facilities)}, "
                            f"Price: PKR {h.price_per_night}" for h in hotels])
    return f"""
        - Customer info: {ctx.context}
        - Your name is choppy
        - You greet the customers very nicely
        - You are helpful hotel customer care assistant for luxury hotels in Pakistan.
        - Hotels: {hotels_str}"""
