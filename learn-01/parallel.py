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
        },
        {
            "name": "list_calendar_events",
            "description": "List all calendar events on a given date.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "format": "date"},
                },
            "required": ["date"],
            },
        },
    ]

def run_tool(name, tool_input):
    if name == "create_calendar_event":
        return {"status": "created", "title": tool_input["title"]}
    elif name == "list_calendar_events":
        return {"events": [{"title": "Existing meeting", "start": "14:00", "end": "15:00"}]}
    
    return {"error": f"Unknown tool {name}"}

def create_message(client, messages):
    return client.messages.create(
        model="claude-opus-4-6",
        tools=tools,
        max_tokens=1024,
        messages=messages,
    )
    

def main():
    client = Anthropic()
    
    print("created anthropic client")

    messages = [
            {
                "role": "user",
                "content": "Check what I have next Monday, then schedule a planning session that avoids any conflicts."
            }
        ]

    response = create_message(client, messages)

    print(response.content)
    print(response.stop_reason)

    while response.stop_reason == "tool_use":
        tool_use_blocks = [tool_use_block for tool_use_block in response.content if tool_use_block.type == "tool_use"]
        tool_call_results = [run_tool(tool_use_block.name, tool_use_block.input) for tool_use_block in tool_use_blocks]
        
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
