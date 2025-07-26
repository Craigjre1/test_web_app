import ollama
import re

SYSTEM_PROMPT = """You are a smart AI agent that can use tools to answer questions.

You must think step by step. Use the following format:

Thought: <your reasoning>
Action: <tool name>
Action Input: <input for the tool>
After this - PAUSE. The tool you have selected will be called and return an observation to you."""

SYSTEM_PROCEED_TEXT = """Following this observation, if you have sufficient information to proceed to a final
answer, return your final answer in the following format:

Final answer: <your final answer>

If you do not have enough, continue through the same chain of reasoning and a further
observation will be returned to you to assist you in arriving at a final answer.

"""

REGEX_TOOL_PATTERN=r"Action: (\w+)\s*Action Input: (.*)"
REGEX_ANSWER_PATTERN=r"Final answer: (.*)"

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

            observation = self.execute_action(response)
            self.messages.append({"role": "agent", "content": observation})


    def execute_action(self,agent_response):




        tool_response = "test"

        observation = tool_response + "\n" + SYSTEM_PROCEED_TEXT
        return observation


            




