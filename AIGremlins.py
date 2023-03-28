"""
A class with a decorator that will try to fix a function using OpenAI.
Executes dynamically generated code in the namespace it was called from.
Don't use this for production code, it's a proof of concept.
"""

import openai
import re
import inspect

class AIGremlin:
    def __init__(
        self,
        api_key,
        max_iterations=3,
        max_tokens=2000,
        temperature = 0.2,
        temperature_escalation = 0.0,
        verbose=False,
        instructions=''
    ):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.max_iterations = max_iterations
        self.max_tokens = max_tokens
        self.tokens = 0
        self.func_tracker = ""
        self.iterations = 0
        self.namespace = ""
        self.verbose = verbose
        self.default_temperature = temperature
        self.temperature = self.default_temperature
        self.temperature_escalation = temperature_escalation
        self.instructions = instructions
        self.functions = {}

    def prompt_format(self, error, func, *args, **kwargs):
        """The prompt to OpenAI for error correcting the error. """

        prompt = f"""While executing the following code:\n {func}
        \nwith the parameters:({args}, {kwargs})
        \nThe following error was encountered:
        \n--{error}--
        Provide a fix by creating a new function that solves the error.
        Stay as close as possible to the intent of the original function, if it is indicated in the doc string.
        Only fix the error, don't remove for example other function calls within the function.
        Only respond with the function, don't give an explanation.
        {self.instructions}
        Always add a decorator again above the function, like this.
        """
        return prompt

    def get_ai_response(self, prompt, temperature):
        """The function that will call OpenAI and return the response."""
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=int(len(prompt) * 2),
        )
        if self.verbose:
            print(response.choices[0].text)
        return {
            "response": response.choices[0].text,
            "tokens": response.usage.total_tokens,
        }

    def get_function_name(self, func):
        match = re.search(r"def\s+(\w+)\(", func)
        if match:
            return match.group(1)

    def update_temperature(self):
        if((self.temperature + self.temperature_escalation) < 1.0):
            self.temperature += self.temperature_escalation

    def ai_backstop(self, func):
        """
        The decorator function that will be used to wrap the function that needs to be backstopped. It tries to fix the function
        using OPEN ai, and will add the same decorator to the new function. It will also add and execute new function to the namespace it
        was originally called from.
        """
        try:
            # This try block will only run on the first iteration of the decorator. All values are set to defaults.

            source_code = inspect.getsource(func)
            self.namespace = func.__globals__
            self.iterations = 0
            self.temperature = self.default_temperature

        except Exception as e:
            # Dynamically executed code cannot be inspected, so we need to get the source code from a dictionary.
            source_code = self.functions[func.__name__]

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result

            except Exception as e:
                if self.iterations > self.max_iterations:
                    print(
                        f"{self.iterations} iterations and {self.tokens} tokens used, stopping"
                    )
                    return
                self.iterations += 1

                prompt = self.prompt_format(e, source_code, *args, **kwargs)
                response = self.get_ai_response(prompt=prompt, temperature=self.temperature)
                self.update_temperature()

                self.functions[func.__name__] = response["response"]
                self.tokens += response["tokens"]

                print("Local code failed, using AI code")
                if self.verbose:
                    print("Error was: ", e)
                    print("Iteration: ", self.iterations)
                    print(
                    f"{response['tokens']} tokens used, total: {self.tokens} tokens used of a max of {self.max_tokens}")
                print("Changing function to ", self.functions[func.__name__])

                # function_name = self.get_function_name(self.functions[func.__name__])
                exec(self.functions[func.__name__], self.namespace)
                new_function = self.namespace[func.__name__]
                result = new_function(*args, **kwargs)
                return result

        return wrapper
