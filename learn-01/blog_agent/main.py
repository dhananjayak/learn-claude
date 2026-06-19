
from dotenv import load_dotenv
from blog_agent.agent import Agent

load_dotenv()  # Load environment variables from .env file

def main():
    agent = Agent(
        system_prompt="You are a research assistant that helps gather information and insights on various topics. You can search the web, summarize articles, and provide detailed explanations based on your findings."
    )

    prompt = "Please provide a summary of the latest advancements in AI research."
    response = agent.invoke(prompt)
    print("Agent response:")
    print(response)

    

if __name__ == "__main__":
    main()