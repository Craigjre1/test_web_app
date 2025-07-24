import ollama

SYSTEM_PROMPT = """You are a smart AI agent that can use tools to answer questions. Your observations can ONLY
come from the output of using a tool - do NOT guess. If no observations come back, continue with your reasoning
you'll have the opportunity to iterate and re-use a tool and try again with different queries or parameters.

You must think step by step. Use the following format:

Thought: <your reasoning>
Action: <tool name>
Action Input: <input for the tool>
Observation: <result of a tool>
... (repeat Thought/Action/Observation as needed).
Final Answer: <your final answer>

Available tools:
- search_tool(query: str): Searches the web for weather information.
- convert_to_F(temp: float): Converts celsius to farenheit.

If no response from a tool, say so - do not guess a result.
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
    history = [SYSTEM_PROMPT,f'User query: {user_query}']

    for step in range(max_steps):
        prompt = "\n".join(history)

    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        options={'temperature': 0}
)          
    return response['message']['content']

tool_map = {"search_tool":search_tool,
            "convert_to_F":convert_to_F
}


user_input = input("What weather question would you like to ask? ")
print(react_agent(user_input,1))