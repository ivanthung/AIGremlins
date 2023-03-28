from AIGremlins import AIGremlin
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
API_KEY = os.getenv("open_ai_key")
MAX_ITERATIONS = 4

gremlin = AIGremlin(api_key=API_KEY,
                    max_iterations=MAX_ITERATIONS,
                    verbose=True,
                    )

@gremlin.ai_backstop
def funcb():
    x = 1
    print("Namespace is working!!")

@gremlin.ai_backstop
def test_func(df, b) -> int:
    """ This function should only return the first column of the dataframe"""
    for i in range(b):
        print(b + 's')
    print(df)
    return c

if __name__ == "__main__":
    a = [{"a": 1, "b": 2}]
    b = pd.DataFrame(a)
    print(test_func(b, 2))
