import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions,call_function 
import sys





def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    if not api_key:
        raise RuntimeError('No API key!')
    client = genai.Client(api_key = api_key)


    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument('user_prompt', type=str, help='User prompt')
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

    for _ in range(20):
        response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt)
    )
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        if response.usage_metadata and args.verbose:

            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
            print(f'Response: {response.text}')
        if response.function_calls:
            function_call_results = []
            for function_call in response.function_calls:
                results = call_function(function_call, verbose=args.verbose)
                if not results.parts:
                    raise Exception("No parts in function call result")
                if results.parts[0].function_response is None:
                    raise Exception("No function response")
                if results.parts[0].function_response.response is None:
                    raise Exception("No response in function response")
                function_call_results.append(results.parts[0])
                if args.verbose:
                    print(f"-> {results.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_call_results))
        else:
            print(response.text)
            return
    print("Agent failed to produce a final response within 20 iterations")
    sys.exit(1)

    


if __name__ == "__main__":
    main()
