import logging
from agents import RunContextWrapper, function_tool
from fileReaders.filereaders import orders

# error function for get_order_status function
# runs when the order id is invalid
def order_error_function(ctx:RunContextWrapper,error:Exception):
    return f"Oops! {error}"

# checks if the query is about order or not then decides if the get_order_status function would work or not
def toggle(ctx:RunContextWrapper,tool):
    query = ctx.context["input"]
    return any(word in query.lower() for word in ["order","orders", "buy", "purchase"])

# function to fetch the status of order by using order ID
@function_tool(is_enabled=toggle,failure_error_function=order_error_function)
async def get_order_status(order_id:str):
    """
    stimulates fetching order status
    Args:
    order_id:str
    """
    logging.info("Tool is called.")
    if order_id not in orders["orders"]:
        logging.info("Order ID not found.")
        raise ValueError("Order ID not found for customer")
    return f"{orders["orders"][order_id]}"