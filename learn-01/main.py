from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def main():

    client = Anthropic()
    model = "claude-sonnet-4-5"

    print("created anthropic client")

    message = client.messages.create(
        model=model,
        max_tokens=1,
        messages=[
            {
                "role": "user",
                "content": "What is latin for Ant? (A) Apoidea, (B) Rhopalocera, (C) Formicidae"
            },
            {
                "role": "assistant",
                "content": "The answer is ("
            }
        ]
    )

    print(message.content)
    print(message.stop_reason)


if __name__ == "__main__":
    main()
