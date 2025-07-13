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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns content of the specified file through the file path, constrained and relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to get the content from, relative to the working directory."
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a specified file's content with the new specified content, constrained to the working directory. If no file or path to the file exists, directories and file will be created and specified content added.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to get the content from, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to overwrite the specified file with, or to add to the newly created file."
            )
        }
    )
)

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file (.py), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to get the content from, relative to the working directory."
            )
        }
    )
)

#list of available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python
    ]
)

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file

working_directory = os.path.dirname(os.path.abspath(__file__))

function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
}

#response generator
for i in range(20):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for function in response.function_calls:
                fn_name = function.name
                args = function.args
                fn = function_map[fn_name]
                result = fn(working_directory, **args)
                messages.append(types.Content(
                    parts=[types.Part(text=str(result))],
                    role='model'
                    )
                )
                print(f" - Calling function: {function.name}({function.args})")
        else:
            if response.text:
                if verbose:
                    print(f"User prompt: {user_prompt}")
                print(f"Final result: \n{response.text}")
                if verbose:
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            break

    except Exception as e:
        print(f"Error: {str(e)}")
        pass
