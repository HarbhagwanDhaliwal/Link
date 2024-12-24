import os
from enum import Enum

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHAINBASE_API_URL = os.getenv('CHAINBASE_SQL_BASE_URL')
CHAINBASE_API_WEB3_URL = os.getenv('CHAINBASE_WEB3_BASE_URL')
CHAINBASE_API_KEY = os.getenv('CHAINBASE_API_KEY')

API_TIME_LIMIT = 20
MAX_COLUMN_SHOW = 4
MAX_TABLE_SHOW = 2
MAX_ROW_SHOW = 20
API_TIMEOUT = 120


class ChainNetworkID(Enum):
    Ethereum = 1
    Eth = 1
    Polygon = 137
    BSC = 56
    Avalanche = 43114
    Arbitrum_One = 42161
    Optimism = 10
    Base = 8453
    zkSync = 324
    Merlin = 4200
