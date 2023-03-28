from AIGremlins import AIgremlin
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
API_KEY = os.getenv("open_ai_key")
MAX_ITERATIONS = 2

gremlin = AIgremlin(api_key=API_KEY, max_iterations=MAX_ITERATIONS)

def funcb():
    print("Namespace is working!!")

@gremlin.ai_backstop
def test_func(df, b) -> int:
    """ This function should only return the first column of the dataframe"""
    funcb()
    print(df)
    return c

if __name__ == "__main__":
    # test_func(1,2)
    a = [{"a": 1, "b": 2}]
    b = pd.DataFrame(a)
    print(test_func(b, 2))

    # testgremlin.get_ai_response("", prompt="hello")
