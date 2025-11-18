def EOLAttachmentBody(plant=196):
    return f"""
        SELECT top(1000)
            [Timestamp],
            [18236] AS ScrawTCorr2PCorrJig2Average
        FROM [WAREHOUSE].[dbo].[{plant}]
        ORDER BY [Timestamp] desc
    """

def EOLAttachmentBodyForTrain(plant=196):
    return f"""
        SELECT [Timestamp], [18236] AS ScrawTCorr2PCorrJig2Average
        FROM [WAREHOUSE].[dbo].[{plant}]
        WHERE [Timestamp] >= ? AND [Timestamp] <= ?
        ORDER BY [Timestamp]
    """
