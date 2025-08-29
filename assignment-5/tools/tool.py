from agents import function_tool
from config.config import tavily_client

@function_tool
def webSearchtool(input:str)->str:
    "Takes input from Runner and returns the result using tavily"
    response = tavily_client.search(input)
    content = ""
    for result in response["results"]:
        content += result["content"]
    return content


