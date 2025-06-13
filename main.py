import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from sys import *
from google.genai import types

verbose = False

if len(argv) < 2: #or (len(argv) = 2 and argv[1] == "--verbose"):
    print("Error: Input requires prompt for model")
    exit(1)
elif len(argv) == 3 and argv[2] == "--verbose":
    verbose = True

user_prompt = argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages    
)
if verbose == True:
    print(f"User prompt: {user_prompt}")
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)