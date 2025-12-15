import pandas as pd
import sqlalchemy

def run_query(engine, query_str, params=None):
    pd.set_option('display.width', 2000)    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    with engine.connect() as connection:
        df = pd.read_sql(query_str, con=connection, params=params)
        return df

