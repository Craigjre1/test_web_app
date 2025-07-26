import ollama
import re

SYSTEM_PROMPT = """You are a smart AI agent that can use tools to answer questions.

You must reason step by step and pause after each tool call. Use exactly this format and stop after providing an Action Input. 
Do not continue until you receive an Observation from the user. Keep your thoughts relatively short.

Thought: <your reasoning>
Action: <tool name>
Action Input: <input for the tool, must use positional arguments>

Then STOP. Wait for the user to provide an Observation before continuing.
"""

SYSTEM_PROCEED_TEXT = """Following this observation, if you have sufficient information to proceed to a final
answer, return your final answer in the following format:

Final answer: <your final answer>

If you do not have enough, continue through the same chain of reasoning and a further
observation will be returned to you to assist you in arriving at a final answer. DO NOT GUESS AN ANSWER.

"""

REGEX_TOOL_PATTERN=r"Action: (\w+)\s*Action Input: (.*)" #extracts the tool and the tool input
REGEX_ANSWER_PATTERN=r"Final answer: (.*)" #extracts the final answer

model_name = "phi3:mini"

class ReactAgent:
    def __init__(self,max_iterations,available_tool_description,available_tool_dict,ollama_model,temp):
        self.system_prompt = SYSTEM_PROMPT + "\n" + available_tool_description
        self.iterations = max_iterations
        self.model = ollama_model
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.available_tools = available_tool_dict
        self.temp = temp


    def __call__(self,user_input):
        self.messages.append({"role": "user", "content": user_input})
        
        for step in range(self.iterations):

            response = ollama.chat(
            model=self.model,
            messages=self.messages,
            options={'temperature': self.temp})
            content = response['message']['content']
            print("printing:" + content)

            self.messages.append({"role": "assistant","content":content})
            action_result = self.execute_action(content)
            if action_result[1]==1:
                return action_result[0]
            
            self.messages.append({"role": "user", "content": action_result[0]})
            print("printing:" + action_result[0])


    def execute_action(self,agent_observation):

        #search for a final answer
        final_answer = re.search(REGEX_ANSWER_PATTERN,agent_observation,re.DOTALL)
        if final_answer:
            return [final_answer.group(1).strip(),1]
        
        #If no final answer, extract tool and tool input
        action_match = re.search(REGEX_TOOL_PATTERN,agent_observation,re.DOTALL)
        if not action_match:
            return ["Error, unable to parse response",0]

        tool_selection = action_match.group(1).strip()
        tool_input = action_match.group(2).strip()

        if tool_selection not in self.available_tools:
            return [f'Error: Unknown tool {tool_selection}',0]

        tool_response = self.available_tools[tool_selection](tool_input)

        tool_output = f'{tool_selection} response: {tool_response}, {SYSTEM_PROCEED_TEXT}'
        return [tool_output,0]


            




