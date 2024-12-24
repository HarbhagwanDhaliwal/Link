import aiohttp
import asyncio
import logging

from config import CHAINBASE_API_WEB3_URL, CHAINBASE_API_KEY, API_TIMEOUT, FLOCK_AUTH_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the system prompt from the file
system_prompt_file = "apis/system_prompt_with_table_data.txt"

with open(system_prompt_file, "r") as f:
    system_prompt_for_ai = f.read()


# Timeout for API requests
TIMEOUT = aiohttp.ClientTimeout(total=API_TIMEOUT)
TIMEOUT_FOR_AI = aiohttp.ClientTimeout(total=40)



# Function to fetch block details
async def api_get_block_by_number(number, chain_id):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "number": number,
        "chain_id": chain_id,
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/block/detail", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while fetching block details")
            return {'Error': "Request timed out while fetching block details"}
        except Exception as e:
            logging.error(f"Failed to fetch block details: {e}")
            return {'Error': f"Failed to fetch block details: {e}"}


# Function to fetch transaction details
async def api_get_transaction(tx_hash, chain_id, block_number=None, tx_index=None):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "hash": tx_hash,
        "chain_id": chain_id,
        "block_number": block_number if block_number is not None else "",
        "tx_index": tx_index if tx_index is not None else ""
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/tx/detail", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while fetching transaction details")
            return {'Error': "Request timed out while fetching transaction details"}
        except Exception as e:
            logging.error(f"Failed to fetch transaction details: {e}")
            return {'Error': f"Failed to fetch transaction details: {e}"}


# Function to fetch native token balances
async def api_get_native_token_balance(address, chain_id, to_block="latest"):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "address": address,
        "chain_id": chain_id,
        "to_block": to_block,
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/account/balance", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while fetching native token balance")
            return {'Error': "Request timed out while fetching native token balance"}
        except Exception as e:
            logging.error(f"Failed to fetch native token balance: {e}")
            return {'Error': f"Failed to fetch native token balance: {e}"}


# Function to fetch token metadata
async def api_get_token_metadata(contract_address, chain_id):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "contract_address": contract_address,
        "chain_id": chain_id,
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/token/metadata", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while fetching token metadata")
            return {'Error': "Request timed out while fetching token metadata"}
        except Exception as e:
            logging.error(f"Failed to fetch token metadata: {e}")
            return {'Error': f"Failed to fetch token metadata: {e}"}


# Function to fetch token price
async def api_get_token_price(contract_address, chain_id):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "contract_address": contract_address,
        "chain_id": chain_id,
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/token/price", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while fetching token price")
            return {'Error': "Request timed out while fetching token price"}
        except Exception as e:
            logging.error(f"Failed to fetch token price: {e}")
            return {'Error': f"Failed to fetch token price: {e}"}


# Function to fetch NFT metadata
async def api_get_nft_metadata(contract_address, nft_id, chain_id):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "contract_address": contract_address,
        "token_id": nft_id,
        "chain_id": chain_id,
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/nft/metadata", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while fetching NFT metadata")
            return {'Error': "Request timed out while fetching NFT metadata"}
        except Exception as e:
            logging.error(f"Failed to fetch NFT metadata: {e}")
            return {'Error': f"Failed to fetch NFT metadata: {e}"}


# Function to resolve ENS domain
async def api_resolve_ens_domain(domain, chain_id, to_block="latest"):
    headers = {
        "x-api-key": CHAINBASE_API_KEY,
    }
    querystring = {
        "domain": domain,
        "chain_id": chain_id,
        "to_block": to_block,
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get(f"{CHAINBASE_API_WEB3_URL}/ens/records", headers=headers,
                                   params=querystring) as response:
                return await response.json()
        except asyncio.TimeoutError:
            logging.error("Request timed out while resolving ENS domain")
            return {'Error': "Request timed out while resolving ENS domain"}
        except Exception as e:
            logging.error(f"Failed to resolve ENS domain: {e}")
            return {'Error': f"Failed to resolve ENS domain: {e}"}

# Function to interact with AI API for help users
async def api_flock_ai(user_query, system_prompt=system_prompt_for_ai):
    api_url = "https://vatsalkshah--flock-chainbase-task-model-api.modal.run/inference"

    # Request body in JSON format
    json_body = {
        "system_prompt": system_prompt,
        "content": user_query
    }

    # Headers with Authorization token
    headers = {
        "Authorization": f"Bearer {FLOCK_AUTH_TOKEN}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    async with aiohttp.ClientSession(timeout=TIMEOUT_FOR_AI) as session:
        try:
            # Send POST request with JSON body and headers
            async with session.post(api_url, json=json_body, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if "content" in data:
                        return data["content"]
                    else:
                        logging.error("Response does not contain 'content' key")
                        return {'Error': "Response does not contain 'content' key"}
                else:
                    # Log the full response details for debugging
                    logging.error(f"Unexpected response status: {response.status}")
                    logging.error(await response.text())  # Log body for further debugging
                    return {'Error': f"Unexpected response status: {response.status}"}
        except asyncio.TimeoutError:
            logging.error("Request timed out while generating SQL query")
            return {'Error': "Request timed out while generating SQL query"}
        except Exception as e:
            logging.error(f"Failed to generate SQL query: {e}")
            return {'Error': f"Failed to generate SQL query: {e}"}

