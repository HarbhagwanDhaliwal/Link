from apis.api_sql import execute_query_and_fetch_results
from bot import run_bot
import asyncio
from utils import get_table


async def test_query():
    sql_query = """
                SELECT * FROM bsc.transactions
                WHERE from_address = "0x82012708dafc9e1b880fd083b32182b869be8e09"
                AND to_address="0x0000000000000000000000000000000000001000"
                AND method_id = "0xf340fa01"
                LIMIT 10
            """
    response = await execute_query_and_fetch_results(sql_query)

    if response and response['Data']:
        # Access columns and data
        columns = response['Columns']
        column_names = [item['name'] for item in columns]
        data = response['Data']
        table = get_table(column_names, data).to_string()
    else:
        print('Failed to retrieve API data.')


if __name__ == '__main__':
    # test query

    # asyncio.run(test_query())

    # run bot
    run_bot()
