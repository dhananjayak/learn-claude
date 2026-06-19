
import os
from anthropic import Anthropic

class Agent:
    def __init__(self, system_prompt: str, model_name: str = "claude-sonnet-4-5", tools: list = None):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model_name = model_name
        self.tools = tools if tools is not None else []
        self.system_prompt = system_prompt
        self.messages = []

    def append_message(self):
        print("Invoking LLM with the following messages:")
        for msg in self.messages:
            print(f"  {msg['role']}: {msg['content']}") 
            
        response = self.client.messages.create(
            model=self.model_name,
            system=self.system_prompt,
            messages=self.messages,
            max_tokens=10240,
            tools=self.tools
        )
        print(f"Invoked LLM, received response: {response.content}")
        return response


    def create_message(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        response = self.append_message()

        while response.stop_reason == "pause_turn":
            self.messages.append({"role": "assistant", "content": response.content})
            response = self.append_message()

        text = []
        for content in response.content:
            if hasattr(content, "text"):
                text.append(content.text)
        return "".join(text)