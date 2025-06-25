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

#system prompt to tell the AI it's role and what to do.
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#schema for functions, i.e. tells the LLM how to use the functions
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

#list of available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

#response generator
response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        )
)

if verbose:
    print(f"User prompt: {user_prompt}")
print(response.text)
if response.function_calls:
    print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

