from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

tools = [
    {"type": "web_search_20260209", "name": "web_search"},
    {"type": "web_fetch_20260209", "name": "web_fetch"},
    {
      "name": "summarize", 
      "description" : "Summarizes a given text.", 
      "input_schema": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to be summarized."
            }
        },
        "required": ["text"]
        }
    }
]
     

def summarize(text):
    """
    Summarizes the given text using the Anthropic API.
    Args:
        text (str): The text to be summarized.
    Returns:
        str: The summarized text.
    """
    client = Anthropic()
    model = "claude-sonnet-4-5"
    messages = [
        {
            "role": "user",
            "content": f"summarize the following text: {text}"
        }
    ]
    message = client.messages.create(
        model = model,
        max_tokens = 10240,
        messages = messages
    )
    
    if message.stop_reason == "end_turn":
        return message.content[0].text
    
    return "Unable to summarize the text."

def main():
    client = Anthropic()
    model = "claude-sonnet-4-5"
    messages = [
        {
            "role": "user",
            "content": "Research LangChain vs LlamaIndex and summarize the differences."
        }
    ]
    message = client.messages.create(
        model = model,
        max_tokens = 1024,
        messages = messages,
        tools = tools
    )

    if message.stop_reason == "max_tokens":
        print("The response was cut off due to max tokens limit.")
        return

    while message.stop_reason != "end_turn":
        if message.stop_reason == "tool_use":
            if message.content[0].name == "summarize":
                tool_input = message.content[0].input
                summary = summarize(tool_input["text"])
                message = client.messages.create(
                    model = model,
                    max_tokens = 1024,
                    messages = messages + 
                    message.content + 
                    [{"role": "user", "content": [{"type": "tool_result", "tool_use_id": message.content[0].id, "text": summary }]}]
                )            
            else:
                print(f"Tool {message.content[0].name} is not implemented.")
                break


    print(message)

if __name__ == "__main__":
    main()