from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def add(a, b):
    """Return the sum of two numbers.

    Args:
        a (int | float): First addend.
        b (int | float): Second addend.

    Returns:
        int | float: The sum of `a` and `b`.
    """
    return a + b

def main():
    client = Anthropic()
    model = "claude-sonnet-4-5"
    messages = [
        {
            "role": "user",
            "content": "add 2 and 3"
        }
    ]
    tools = [
            {                
                "name": "add",
                "description": "Add two numbers together.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            }
    ]
    message = client.messages.create(
        model = model,
        max_tokens = 1024,
        messages = messages,
        tools = tools
    )

    print(message)
    if message.stop_reason == "tool_use":
        message.content[0].name == "add"
        tool_input = message.content[0].input
        result = add(tool_input["a"], tool_input["b"])
        print(f"Tool result: {result}")
        messages.append({
            "role": "assistant",
            "content": message.content
        })
        messages.append({
            "role": "user",            
            "content": [{"type": "tool_result", "tool_use_id": message.content[0].id, "content": f"{result}"}]
        })
        result = client.messages.create(
            model = model,
            max_tokens = 1024,
            messages = messages,
        )
        print(result)   

if __name__ == "__main__":
    main()