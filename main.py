import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from config import model_name
from functions.call__function import available_functions
from functions.call__function import call_function

def load_api_key():
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	if not api_key:
		raise RuntimeError("GEMINI_API_KEY environment variable not set")
	return api_key

def main():
	api_key = load_api_key()
	client = build_client(api_key)
	args = load_content_from_args()

	# render user_messages from argument
	messages = [types.Content(role="user", parts=[types.Part(text = args.user_prompt)])]
	if args.verbose:
		print("User prompt:", args.user_prompt)
	
	# AI call
	for _ in range(20):
		response = client.models.generate_content(
			model=model_name, 
			contents=messages, 
			config = get_ai_config()
		)

		if response.candidates:
			for candidate_response in response.candidates:
				messages.append(types.Content(role="model", parts=candidate_response.content.parts))
	
		to_continue, function_call_result = print_ai_response(response, args)
		if not to_continue:
			return 0
		
		messages.append(function_call_result)

	raise RuntimeError("Failed to get a valid response after 20 iterations")

def get_ai_config():
	return types.GenerateContentConfig(
		system_instruction=system_prompt, 
		tools=[available_functions]
	)

def load_content_from_args():
	parser = argparse.ArgumentParser(description = "ShivamCodingAgent")
	parser.add_argument("user_prompt", type = str, help = "User Prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()
	return args 

def handle_function_call(function_call, verbose=False):
	
	function_call_result = call_function(function_call, verbose=verbose)
	if not function_call_result.parts:
		raise RuntimeError("Function call result is missing parts")
	
	if not function_call_result.parts[0].function_response:
		raise RuntimeError("Function call result is missing function response")
	
	if not function_call_result.parts[0].function_response.response:
		raise RuntimeError("Function call result is missing function response content")

	if verbose:
		print(f"-> {function_call_result.parts[0].function_response.response}")

	return function_call_result



def print_ai_response(response, args):
	if response.function_calls:
		for function_call in response.function_calls:
			result = handle_function_call(function_call, args.verbose)
			return True, result
	
	if not response.text:
		raise RuntimeError("Generate Response text is missing")
	if not response.usage_metadata:
		raise RuntimeError("usage metadata is missing in generate response call")
	if args.verbose:
		print("Prompt tokens:", response.usage_metadata.prompt_token_count)
		print("Response tokens:", response.usage_metadata.candidates_token_count)
	
	

	print("Response:")
	print(response.text)
	return False, ""

def build_client(api_key):
	client = genai.Client(api_key=api_key)
	return client
	

if __name__ == "__main__":
	main()
