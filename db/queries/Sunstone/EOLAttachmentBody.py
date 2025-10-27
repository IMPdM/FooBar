def EOLAttachmentBody(plant=196):
    return f"""
        SELECT top(1000)
            [Timestamp],
            [18236] AS ScrawTCorr2PCorrJig2Average
        FROM [WAREHOUSE].[dbo].[{plant}]
        ORDER BY [Timestamp] desc
    """