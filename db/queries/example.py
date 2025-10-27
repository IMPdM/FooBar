def example(table=308):
    return f"""
        SELECT TOP(10) *
        FROM [WAREHOUSE].[dbo].[{table}]
        WHERE [Timestamp] BETWEEN :start_time AND :end_time
    """