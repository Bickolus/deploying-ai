from openai import OpenAI
from dotenv import load_dotenv
from assignment_chat.prompts import return_instructions
import json
import requests
from utils.logger import get_logger
import os


_logs = get_logger(__name__)

load_dotenv(".env")
load_dotenv(".secrets")


client = OpenAI()

open_ai_model = os.getenv("OPENAI_MODEL", "gpt-4")

tools = [
    {
        "type": "function",
        "name": "get_random_swanson_quote",
        "description": "This tool retrieves a random quote said by Ron Swanson",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        
    },

    {
        "type": "function",
        "name": "get_random_swanson_quotes",
        "description": "This tool retrieves a specified number of random Ron Swanson quotes",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",
                    "description": "Number of quotes specified",
                }
            },
            "required": ["number"],
            "additionalProperties": False
        },
        
    },

    {
        "type": "function",
        "name": "get_specific_swanson_quote",
        "description": "This tool retrieves a Ron Swanson quote using a keyword",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Relevant words included in a quote or saying",
                }
            },
            "required": ["keyword"],
            "additionalProperties": False
        },
        
    },
]



def get_random_swanson_quote():
    """
    API Call. Returns a random quote from Ron Swanson, a character from Parks and Recreation.
    """
    url = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
    response = requests.get(url)
    quote = json.loads(response.text)
    return quote



def get_random_swanson_quotes(number:int):
    """
    API Call. Returns an array of random Ron Swanson quotes using the number specified.
    """
    number_string = str(number)
    url = "https://ron-swanson-quotes.herokuapp.com/v2/quotes/"+number_string
    response = requests.get(url)
    quotes = json.loads(response.text)
    return quotes

def get_specific_swanson_quote(keyword:str):
    """
    API Call. Returns an array of quotes from Ron Swanson matching the search term.
    """
    keyword = keyword.lower()
    url = "https://ron-swanson-quotes.herokuapp.com/v2/quotes/search/"+keyword
    response = requests.get(url)
    quotes = json.loads(response.text)
    return quotes

def sanitize_history(history: list[dict]) -> list[dict]:
    clean_history = []
    for msg in history:
        clean_history.append({
            "role": msg.get("role"),
            "content": msg.get("content")
        })
    return clean_history


def swanson_quote_chat(message: str, history: list[dict] = []) -> str:
    _logs.info(f'User message: {message}')
    
    instructions = return_instructions()
    
    user_msg = {
        "role": "user",
        "content": message
    }
    
    conversation_input = sanitize_history(history) + [user_msg]
    
    response = client.responses.create(
        model=open_ai_model,  
        instructions=instructions,
        input=conversation_input,
        tools=tools,
        
    )

    conversation_input += response.output

    # Handle function calls if any
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_random_swanson_quote":
                # Call the quote function
                quote_result = get_random_swanson_quote()
                
                # Add function call result to conversation
                
                func_call_output = {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "quote": quote_result
                    })
                }
                
                _logs.debug(f"Function call output: {func_call_output}")

                conversation_input = conversation_input + [func_call_output]
                
                # Make second API call with function result
                response = client.responses.create(
                    model=open_ai_model,
                    instructions=instructions,
                    tools=tools,
                    input=conversation_input
                )
                break
            
            elif item.name == "get_random_swanson_quotes":
                args = json.loads(item.arguments)
                _logs.info(f'Function call args: {args}')
                
                quote_result = get_random_swanson_quotes(**args)

                func_call_output = {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "quote": quote_result
                    })
                }
                
                _logs.debug(f"Function call output: {func_call_output}")

                conversation_input = conversation_input + [func_call_output]
                
                response = client.responses.create(
                    model=open_ai_model,
                    instructions=instructions,
                    tools=tools,
                    input=conversation_input
                )
                break

            elif item.name == "get_specific_swanson_quote":
                args = json.loads(item.arguments)
                _logs.info(f'Function call args: {args}')
                
                quote_result = get_specific_swanson_quote(**args)

                
                func_call_output = {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "quote": quote_result
                    })
                }
                
                _logs.debug(f"Function call output: {func_call_output}")

                conversation_input = conversation_input + [func_call_output]
                
                response = client.responses.create(
                    model=open_ai_model,
                    instructions=instructions,
                    tools=tools,
                    input=conversation_input
                )
                break
    
    return response.output_text