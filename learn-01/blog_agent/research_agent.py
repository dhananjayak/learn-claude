import asyncio
from claude_agent_sdk import AssistantMessage, query, ClaudeAgentOptions

class ResearchAgent:
    def __init__(self):
        self.agent_name = "Research Agent"
        self.options = ClaudeAgentOptions(
            system_prompt="You are a research assistant that helps gather information and insights on various topics. You can search the web, summarize articles, and provide detailed explanations based on your findings."
        )

    async def perform_research(self, topic: str) -> str:
        messages = []
        try:
            async for message in query(prompt=topic, options=self.options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if hasattr(block, "text"):
                            messages.append(block.text)
        except Exception as exc:
            return f"Error from Claude agent: {exc}"

        if not messages:
            return "No assistant response (empty result)"

        return "\n".join(messages)
                    
