import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

tools = [
        {
            "name": "create_calendar_event",
            "description": "Create a calendar event with attendees and optional recurrence.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": { "type": "string"},
                    "start": { "type": "string", "format": "date-time"},
                    "end": { "type": "string", "format": "date-time"},
                    "attendees": {
                        "type": "array",
                        "items": { "type": "string", "format": "email"}

                    },
                    "recurrence": {
                        "type": "object",
                        "properties": {
                            "frequence": {"enum": ["daily", "weekly", "monthly"]},
                            "count": { "type": "integer", "minimum": 1}
                        }

                    }
                },
                "required": [ "title", "start", "end" ]
            }
        }
    ]

def run_tool(name, tool_input):
    if name == "create_calendar_event":
        return {"status": "created", "title": tool_input["title"]}
    
    return {"error": f"Unknown tool {name}"}

def create_message(client, messages):
    return client.messages.create(
        model="claude-opus-4-6",
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        max_tokens=1024,
        messages=messages,
    )
    

def main():
    client = Anthropic()
    
    print("created anthropic client")

    messages = [
            {
                "role": "user",
                "content": "Schedule a weekly team standup every Monday at 9am for the next 4 weeks. Invite the whole team: alice@example.com, bob@example.com, carol@example.com."
            }
        ]

    response = create_message(client, messages)

    print(response.content)
    print(response.stop_reason)

    while response.stop_reason == "tool_use":
        tool_use = next(tool_use_block for tool_use_block in response.content if tool_use_block.type == "tool_use")
        tool_result = run_tool(tool_use.name, tool_use.input)
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(tool_result)
                }
            ]
        })
        response = create_message(client, messages)

    print(response.content)
    print(response.stop_reason)



    

if __name__ == "__main__":
    main()
