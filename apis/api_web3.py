import aiohttp
import asyncio
import logging

from config import CHAINBASE_API_WEB3_URL, CHAINBASE_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to fetch block details
async def api_get_block_by_number(number, chain_id):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "number": number,
        "chain_id": chain_id,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/block/detail", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except Exception as e:
            logging.error(f"Failed to fetch block details: {e}")
            return {'Error': f"Failed to fetch block details: {e}"}

