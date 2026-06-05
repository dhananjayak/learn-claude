from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def main():
    client = Anthropic()
    model = "claude-sonnet-4-5"
    messages = [
        {
            "role": "user",
            "content": "who is the president of the united states in 2026?"
        }
    ]
    message = client.messages.create(
        model = model,
        max_tokens = 1024,
        messages = messages,
        tools = [
            {"type": "web_search_20260209", "name": "web_search"},
            {"type": "web_fetch_20260209", "name": "web_fetch"}
        ]
    )

    print(message)

if __name__ == "__main__":
    main()