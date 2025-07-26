
from agent import ReactAgent

TOOL_DESCRIPTION = """Available tools:
- search_tool(question: str): Searches the web for information. Returns requested information.
- user_order(agent_prompt): Asks the user what they would like to order. Returns customer order.
- get_account_details(agent_prompt): Asks the user for their account details. Returns user account details.
- make_purchase(account_details: string, store_ID: string, user_order: string) uses account details, store ID and order to
make the purchase. Returns True if successful, False if unsuccessful.
"""

def search_tool(question):
    return "Your nearest Dominos Pizza store ID is 45635678"

def user_order(agent_prompt):
    user_order = input("Agent: " + agent_prompt)
    return user_order

def get_account_details(agent_prompt):
    user_details = input("Agent: " + agent_prompt)
    return user_details

def make_purchase(account_details,store_ID,user_order):
    return True


tool_dict = {"search_tool":search_tool,
             "user_order":user_order,
             "get_account_details":get_account_details,
             "make_purchase":make_purchase
}

OLLAMA_MODEL = "deepseek-r1"

my_agent = ReactAgent(4,TOOL_DESCRIPTION,tool_dict,OLLAMA_MODEL,0)
user_input = input("What would you like to do today? ")
my_agent(user_input)