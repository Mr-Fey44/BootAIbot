import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.config import system_prompt
from call_function import available_functions

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("prompt", help="The user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv() # take environment variables
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key) #creates a new gemini client

    user_prompt = args.prompt

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),] #creates a list of messages

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
    if verbose:
        print(f'User prompt: {messages}')
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
            return response.text

    for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")


if __name__ == "__main__":
    main()
