from dotenv import load_dotenv
import os
load_dotenv()

import pandas as pd
import datetime
from AIGremlins import AIGremlin

gremlin = AIGremlin(api_key=os.getenv("open_ai_key"),
                    max_iterations=10,
                    verbose=True,
                    temperature_escalation=0.2,
                    model='gpt-4'
                    )

@gremlin.ai_backstop
def first_function(df) -> int:
    """ This function should only return the first column of the dataframe"""
    return second_function(
        df['year'],
        df['mont'],
        df['day']
        )
    
@gremlin.ai_backstop
def second_function(year, month, day) -> int:
    """ This function should divide its inputs"""
    return datetime.date(year, month, day)

if __name__ == "__main__":
    dates = pd.DataFrame (
        [{"year": 23, "month": 13, "day": 5}]
        )
    
    result = first_function(dates)
    print(result)




