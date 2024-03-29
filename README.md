# AIGremlins

AI Gremlin - Automatic Error Correction with OpenAI
AI Gremlin is a Python module that leverages OpenAI's GPT-3 to automatically fix errors in your Python code. The module contains the class AIgremlin, which handles exceptions and get suggestions for fixes from OpenAI's API.

Note:
Using this code in real applications is a terrible idea for many reasons, including:
- Creating the machine revolution by given an AI direct possibility to execute functions without anyone chekcing.
- There's no garantuee that the AI generated function won't break anything else or delete something import.
- Many other reasons.

Don't even think about using this in production.

## Installation
```
pip install aigremlins
```

## Example usage
```
from aigremlins import AIGremlin

# Initialize AI Gremlin instance with your OpenAI API key
gremlin = AIgrAIGremlinemlin(api_key="your_openai_api_key", verbose=True)

# Define the function with an error
@gremlin.ai_backstop
def buggy_function(a, b):
    """ This function should always return a value"""
    return a / b

# Call the function with parameters that cause an exception
result = buggy_function(4, 0)
```


### Features
Automatically detects and corrects errors in your Python functions using OpenAI's GPT-3.
Tries to stay as close as possible to the intent of the original function.
Dynamically adds and executes the new fixed function in the original namespace.
Customizable parameters to control the number of iterations, token limit, temperature settings, and verbosity of the output.
Ability to add custom instructions for OpenAI's API.

### How It Works
The AIgremlin class wraps your target function with a decorator called ai_backstop.
When the target function encounters an exception, the ai_backstop decorator captures the error, function code, and parameters.
The ai_backstop decorator formats a prompt for OpenAI's API to get a suggestion for fixing the function.
The suggestion is received from OpenAI's API, and a new fixed function is generated.
The fixed function is added to the original namespace and executed.
The process continues until the fixed function executes without errors or the maximum number of iterations is reached.

### Usage
1. Import the AIgremlin class from the module.
2. Instantiate an AIgremlin object with your OpenAI API key and other optional parameters (e.g., max_iterations, max_tokens, temperature, temperature_escalation, verbose, and instructions).
3. Define your function and apply the ai_backstop decorator to it.

Call the decorated function as you normally would. If an exception is encountered, the AI Gremlin will automatically attempt to fix it using OpenAI's API.


### Options
1. temperature -> default temperature of the model used.
2. temperature escalation -> the model can become increasingly creative. Should be somewhere between the range of 0.1-0.4 as the max temperature is 1.
3. instructions -> you can give additional instructions to the AI to take into consideration.