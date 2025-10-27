import json
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_engine():
    with open("config/db_connection.json") as file:
        config = json.load(file)

    connection_url = URL.create(
        "mssql+pyodbc",
        username=config["User_ID"],
        password=config["Password"],
        host=config["Server"],
        database=config["Database"],
        query={"driver": "SQL Server"}
 )

    return create_engine(connection_url)
