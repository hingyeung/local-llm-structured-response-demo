from langchain_experimental.llms.ollama_functions import OllamaFunctions

from config import choose_model
from tools.toolbox import TOOL_NAMES_TO_FUNCTIONS

MODEL_NAME = "llama3:latest"

model = OllamaFunctions(
    model=MODEL_NAME,
    format="json",
)

# provide a list of tools to bind to the model
model = model.bind_tools(
    tools=[
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get the weather for."
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celcius", "fahrenheit"],
                    }
                },
                "required": ["location"],
            }
        },
        {
            "name": "get_today_pollen_level",
            "description": "Get today's pollen level in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get the pollen level for."
                    },
                },
                "required": ["location"],
            }
        },
        {
            "name": "get_current_population",
            "description": "Get the current population in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get the population for."
                    }
                },
                "required": ["location"],
            }
        }
    ],
    # https://python.langchain.com/v0.2/docs/integrations/chat/ollama_functions/
    # function_call parameter to force the model to call the given function
    # function_call={"name": "get_current_weather"},
)

def explain_tool_calls_in_model_response(model_response, call_function=False):
    if model_response.tool_calls is None:
        print("The model did not choose to use any tools.")
        return
    
    tool_name = model_response.tool_calls[0]["name"]
    function_args = model_response.tool_calls[0]["args"]
    print(f"The model has chosen to use tool: {tool_name}")
    print(f"The function for the tool is: {TOOL_NAMES_TO_FUNCTIONS[tool_name]}")
    print(f"The function args are as follows: {function_args}")
    if call_function is True:
        print(f"The result of the function is: {TOOL_NAMES_TO_FUNCTIONS[tool_name](**function_args)}")
    print("")

chosen_model = choose_model(standalone_mode=False)

# invoke the model with a question, hopefully it will use the right tool
explain_tool_calls_in_model_response(model.invoke("What is the current weather in New York City?"), True)
explain_tool_calls_in_model_response(model.invoke("What is the current pollen level in New York City?"), True)
