
import asyncio
from claude_agent_sdk import AssistantMessage, query, ClaudeAgentOptions


async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a research assistant that helps gather information and insights on various topics. You can search the web, summarize articles, and provide detailed explanations based on your findings."
    )

    topic = "What are the latest advancements in artificial intelligence research?"
    async for message in query(prompt=topic, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)


if __name__ == "__main__":
    asyncio.run(main())