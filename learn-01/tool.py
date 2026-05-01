import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

def main():

    client = Anthropic()
    
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

    print("created anthropic client")

    response = client.messages.create(
        model="claude-opus-4-6",
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am."
            }
        ],
    )

    print(response.content)
    print(response.stop_reason)

    tool_uses = [tool_use for tool_use in response.content if tool_use.type == "tool_use"]
    

    print(tool_uses)
    

    result = client.messages.create(
        model="claude-opus-4-6",
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Schedule a 30-minute sync with alice@example.com and bob@example.com next Monday at 10am."
            },
            {
                "role": "assistant",
                "content" : response.content
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_uses[0].id,
                        "content": json.dumps({"event_id": "evt_123", "status": "created"})
                    }
                ]
            }
        ],
    )

    print(result.content)
    print(result.stop_reason)


if __name__ == "__main__":
    main()
