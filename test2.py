import ollama

SYSTEM_PROMPT = """You are a smart AI agent that can use tools to answer questions.

You must think step by step. Use the following format:

Thought: <your reasoning>
Action: <tool name>
Action Input: <input for the tool>
Observation: <result of tool>
... (repeat Thought/Action/Observation as needed).
Final Answer: <your final answer>

Available tools:
- search_tool(query: str): Searches the web for weather information.
- convert_to_F(temp: float): Converts celsius to farenheit.
"""

search_return_dict= {1:"Unable to return suitable search results for your query",
                     2:"The highest temperature in Spain today is 30 degrees celsius",
                     3:"The highest temperature in Harlow today is 20 degrees celsius"
}

def search_tool(pass_no,question):
    return search_return_dict[pass_no]

def convert_to_F(temp):
    farenheit = temp*9/5 + 32
    return farenheit

def react_agent(user_query,max_steps):
    return 1

user_input = input("What weather question would you like to ask? ")
print(react_agent(user_input,5))