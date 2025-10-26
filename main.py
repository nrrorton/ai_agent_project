import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
)


def main():
    # Load environment variables
    load_dotenv()

    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Make sure it's in your .env file.")
    
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )


    parser = argparse.ArgumentParser(description="Send a prompt to Gemini-2.0-flash-001.")
    parser.add_argument("prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    user_prompt = " ".join(sys.argv[1:])
    verbose = args.verbose

    # Initialize Gemini client
    client = genai.Client(api_key = api_key)

    system_prompt = """
    You are a helpful AI coding agent working in a restricted environment.

    You have access to the following tools and can use them when necessary:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    Your working directory is the 'calculator' folder. All file paths must be relative to that directory.
    You do NOT need to specify the working directory argument when calling functions; it will be injected automatically.

    When a user reports a bug or asks about code behavior:
    1. Examine the project files using `get_files_info` and `get_file_content`.
    2. Analyze the code logically to understand the issue.
    3. If appropriate, fix the problem by calling `write_file` with the corrected code.
    4. Optionally, test the program afterward using `run_python_file` to verify the fix.
    5. Always explain your reasoning clearly and concisely.
    """


    MAX_ITERATIONS = 3
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for iteration in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            # Check for function calls first
            if hasattr(response, "function_calls") and response.function_calls:
                for fn_call in response.function_calls:
                    function_call_result = call_function(fn_call, verbose=verbose)

                    # Validate function response
                    try:
                        resp_dict = function_call_result.parts[0].function_response.response
                    except Exception:
                        raise RuntimeError("Fatal: function call result is malformed.")

                    # Append the function result as a new message
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part(text=str(resp_dict))]
                        )
                    )

                    if verbose:
                        print(f" - Calling function: {fn_call.name}")
                        print(f"-> {resp_dict}")

            # Now handle any plain text output
            text_parts = []
            for candidate in getattr(response, "candidates", []):
                # candidate.content may be a tuple
                contents = candidate.content
                if isinstance(contents, tuple):
                    contents = list(contents)  # make it iterable
                for part in contents:
                    if hasattr(part, "text") and part.text:
                        text_parts.append(part.text.strip())

            if text_parts:
                final_text = "\n".join(text_parts)
                print("Final response:")
                print(final_text)
                break

        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {e}")
            break

    # Verbose output
    if verbose:
        print(f'User prompt: "{user_prompt}"')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
