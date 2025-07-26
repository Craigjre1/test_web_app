
from agent import ReactAgent

TOOL_DESCRIPTION = """Available tools:
- search_tool(query: str): Searches the web for information. Returns requested information.
- get_storeID(location_details: string) takes the location details of the store and returns the store ID.
- user_order(): Asks the user what they would like to order. Returns customer order.
- get_account_details(): Asks the user for their account details. Returns user account details.
- make_purchase(account_details: string, store_ID: string, user_order: string) uses account details, store ID and order to
make the purchase. Returns True if successful, False if unsuccessful.
"""

def search_tool(pass_no,question):
    return "Your nearest Dominos Pizza is in The Stow, Harlow"

def get_storeID(location_details):
    return "The store ID is 12345678"

def user_order():
    user_order = input("What would you like to order: ")
    return user_order

def get_account_details():
    user_details = input("What are your account details? ")
    return user_details

def make_purchase(account_details,store_ID,user_order):
    return True


tool_dict = {"search_tool":search_tool,
             "get_storeID":get_storeID,
             "user_order":user_order,
             "get_account_details":get_account_details,
             "make_purchase":make_purchase#
}

OLLAMA_MODEL = "phi3:mini"

my_agent = ReactAgent(3,TOOL_DESCRIPTION,tool_dict,OLLAMA_MODEL,0)
user_input = input("What would you like to do today? ")
my_agent(user_input)