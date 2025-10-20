import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    parser = argparse.ArgumentParser(description="Send a prompt to Gemini-2.0-flash-001.")
    parser.add_argument("prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    user_prompt = " ".join(sys.argv[1:])
    verbose = args.verbose

    # Initialize Gemini client
    client = genai.Client(api_key = api_key)

    messages = [
        types.Content(role = "user", parts = [types.Part(text = user_prompt)]),
    ]

    # Generate content
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages
    )

    # Display results
    print(response.text)

    # Verbose output
    if verbose:
        print(f'User prompt: "{user_prompt}"')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
