import pandas as pd
from sqlalchemy import text

def run_query(engine, query_str, params=None):
    pd.set_option('display.width', 2000)    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    with engine.connect() as connection:
        df = pd.read_sql(text(query_str), con=connection, params=params)
        return df

