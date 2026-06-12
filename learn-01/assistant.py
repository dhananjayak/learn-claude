import os
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

GREET_AND_ASK_USER_INFO = "Hello! You are helping a user set up their assistant profile. Please ask the user for their name and email address, and then create an assistant profile using that information."

class AssistantProfile(BaseModel):
    name: str
    email: str
    history: list = []

load_dotenv()

EXTRACT_USER_PROFILE_INSTRUCTIONS = """
Please extract the user's name and email address from the following message:
{{user_message}}

The output should be a JSON object with the following format:
{
    "name": "User's name",
    "email": "User's email address"
}
"""

def main():
    if not assistant_profile_exists():
        extract_profile()
    profile = AssistantProfile.model_validate_json(open("assistant.json").read())
    continue_conversation(profile)

    
    
def assistant_profile_exists():
    return os.path.exists("assistant.json")

def extract_profile():
    client = Anthropic()
    model = "claude-sonnet-4-5"
    
    user_message = input("User: ")
    user_message = EXTRACT_USER_PROFILE_INSTRUCTIONS.replace("{{user_message}}", user_message)  
    messages =  [{
            "role": "user",
            "content": user_message
        }]
    
    message = client.messages.parse(
            model = model,
            max_tokens = 10240,
            system=GREET_AND_ASK_USER_INFO,
            messages = messages,
            output_format = AssistantProfile
    )

    if message.stop_reason == "end_turn":
        try:
            profile_data = message.content[0].text
            profile = AssistantProfile.model_validate_json(profile_data)
            create_assistant_profile(profile.name, profile.email)
        except Exception as e:
            print(f"Error parsing profile data: {e}")
    return profile

def continue_conversation(profile):
    client = Anthropic()
    model = "claude-sonnet-4-5"
    
        
    messages = profile.history[-10:]  # Keep the last 10 messages for context

    print(messages)

    user_message = input("User: ")
    profile.history.append({"role": "user", "content": user_message})
    messages.append({"role": "user", "content": user_message})
    
    message = client.messages.create(
            model = model,
            max_tokens = 10240,
            system=f"You are a helpful assistant assisting {profile.name}.",
            messages = messages
        )
        
    if message.stop_reason == "end_turn":
        assistant_response = message.content[0].text
        print(f"Assistant: {assistant_response}")
        profile.history.append({"role": "assistant", "content": assistant_response})
    else:
        print("Assistant did not respond properly.")

    with open("assistant.json", "w") as f:
        f.write(profile.json())    
    
def create_assistant_profile(name, email):
    profile = AssistantProfile(name=name, email=email)
    with open("assistant.json", "w") as f:
        f.write(profile.json())
    print("Assistant profile created successfully.")

if __name__ == "__main__":
    main()