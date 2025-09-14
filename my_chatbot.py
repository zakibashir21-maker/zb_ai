# yes
import os
from openai import OpenAI

# Load API key from credentials file
CREDENTIALS_FILE = "credentials.txt"

if not os.path.exists(CREDENTIALS_FILE):
    raise FileNotFoundError(f"Credentials file '{CREDENTIALS_FILE}' not found.")

with open(CREDENTIALS_FILE, "r") as f:
    api_key = f.read().strip()


client = OpenAI(api_key=api_key)

end_program = False

while not end_program:
    get_input = input("Enter a prompt: ")
    if get_input.lower() == "goodbye" or get_input.lower() == "exit":
        end_program = True
        print("Savage.AI disliked that.")
    else:
        messages = [
            {"role":"system", "content": "You are a chatbot that roasts the user in the most Passive-Aggressive ways."},
            {"role": "user", "content": get_input}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages
        )
        assistant_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_response})
        print("Assistant: " + assistant_response)
