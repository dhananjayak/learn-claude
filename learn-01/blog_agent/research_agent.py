import asyncio
from claude_agent_sdk import AssistantMessage, query, ClaudeAgentOptions
from agent import Agent

class ResearchAgent(Agent):
    def __init__(self):
        self.tools = [
            {
             "type": "web_search_20250305", 
             "name": "web_search", 
             "max_uses": 3
            },
            {
            "type": "web_fetch_20250910",
            "name": "web_fetch",
            "max_uses": 5,
            "citations": {"enabled": True},
            }
        ]
        super().__init__(
            system_prompt="You are a research assistant that helps gather information and insights on various topics. You can search the web, summarize articles, and provide detailed explanations based on your findings that could be used to create a blog post.",
            tools=self.tools
        )

    def perform_research(self, topic: str):
        result = self.create_message(f"Please provide information about {topic} in about 500 words")

        return result
