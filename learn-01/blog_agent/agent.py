
import os
from anthropic import Anthropic

class Agent:
    def __init__(self, system_prompt: str, model_name: str = "claude-sonnet-4-5"):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model_name = model_name
        self.tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]
        self.system_prompt = system_prompt
        self.messages = []

    def invoke_llm(self):
        print("Invoking LLM with the following messages:")
        for msg in self.messages:
            print(f"  {msg['role']}: {msg['content']}") 
            
        response = self.client.completions.create(
            model=self.model_name,
            system=self.system_prompt,
            messages=self.messages,
            max_tokens=1024,
            tools=self.tools
        )
        print(f"Invoked LLM, received response: {response.completion}")
        return response


    def invoke(self, prompt: str):
        self.messages.append({"role": "user", "content": prompt})
        response = self.invoke_llm()

        if response.stop_reason == "pause_turn":
            self.messages.append({"role": "assistant", "content": response.content})
            response = self.invoke_llm()

        return response.content