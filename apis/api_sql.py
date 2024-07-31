import requests
import aiohttp
import asyncio
import logging

from config import CHAINBASE_API_URL, CHAINBASE_API_KEY, API_TIME_LIMIT

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to execute the query
async def execute_query(sql_query):
    headers = {
        "X-API-KEY": CHAINBASE_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"sql": sql_query}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{CHAINBASE_API_URL}/query/execute", json=data, headers=headers) as response:
                return await response.json()
        except Exception as e:
            print(f"Failed to execute query: {e}")
            return {}


# Function to check the status of the query execution
async def check_status(execution_id):
    headers = {
        "X-API-KEY": CHAINBASE_API_KEY,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{CHAINBASE_API_URL}/execution/{execution_id}/status", headers=headers) as response:
                return await response.json()
        except Exception as e:
            print(f"Failed to check status: {e}")
            return {}


# Function to get the results of the query execution
async def get_results(execution_id):
    headers = {
        "X-API-KEY": CHAINBASE_API_KEY,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{CHAINBASE_API_URL}/execution/{execution_id}/results", headers=headers) as response:
                return await response.json()
        except Exception as e:
            print(f"Failed to get results: {e}")
            return {}


async def execute_query_and_fetch_results(query):
    try:
        sql_query = query
        response = await execute_query(sql_query)

        if 'data' in response and response['data']:
            execution_id = response['data'][0].get('executionId')
            logging.info(f"Execution ID: {execution_id}")

            status = "RUNNING"
            max_try = 0
            while status not in ["FINISHED", "FAILED"]:
                status_response = await check_status(execution_id)
                max_try += 1
                if 'data' in status_response and status_response['data']:
                    status = status_response.get('data', [{}])[0].get('status', 'No status')
                    logging.info(f"Status: {status}")
                    if status not in ["FINISHED", "FAILED"]:
                        await asyncio.sleep(1)

                    if max_try >= API_TIME_LIMIT:
                        break
                else:
                    logging.info("No data found in response of status")
                    break

            if status in ["FINISHED", "FAILED"]:
                results = await get_results(execution_id)
                data = results['data']
                if 'data' in data:
                    if data['data']:
                        columns = data['columns']
                        internal_data = data['data']
                        logging.info(f"Columns: {columns}")
                        logging.info(f"Data: {internal_data}")
                        return {'Columns': columns, 'Data': internal_data}

                    else:
                        message = data['message']
                        logging.info(f"Results: {message}")
                        return {'Error': message}
            else:
                logging.info("Query execution failed")
                return {'Error': "Query execution failed"}
        else:
            logging.info("No data found in response")
            return {'Error': "No data found in response"}

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {'Error': f"An error occurred: {e}"}
