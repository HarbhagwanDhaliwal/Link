---

# Link Discord Bot

We have developed **Link**, a Discord bot that connects with the ChainBase blockchain. It's an open-source project that anyone can use.

## Features

Link bot allows you to interact with blockchain data using a set of powerful commands:

### Available Commands

- **/sql**: Execute the SQL query to show up to 4 columns and 20 rows.
- **/sql_excel**: Execute the SQL query and get the result in an Excel file.
- **/get_block_by_number**: Fetch block details by block number and chain ID.
- **/get_transaction**: Get the details of a transaction given the transaction hash.
- **/get_native_token_balance**: Get the native token balance for a specified address.
- **/get_token_metadata**: Get the metadata of a specified token.
- **/get_token_price**: Get the price of a specified token.
- **/get_nft_metadata**: Get the metadata associated with the specified NFT.
- **/get_domain_metadata**: Resolve an ENS domain to its associated address.

## Setup and Installation

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/HarbhagwanDhaliwal/Link.git
cd Link
```

### Step 2: Set Environment Variables

Set up the following environment variables in your system:

```bash
DISCORD_BOT_TOKEN=your_discord_bot_token
CHAINBASE_SQL_BASE_URL=https://api.chainbase.com/api/v1
CHAINBASE_WEB3_BASE_URL=https://api.chainbase.online/v1
CHAINBASE_API_KEY=your_chainbase_api_key
```

You can obtain the ChainBase API key from the ChainBase console. For the Discord bot token, create a Discord application and generate the token from there.

### Step 3: Install Dependencies

Install the required Python dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Bot

After setting up the environment variables and installing dependencies, run the bot using:

```bash
python main.py
```

## What is ChainBase Data Platform?

ChainBase Data Platform is an all-in-one data infrastructure for Web3 that allows you to index, transform, and utilize large-scale on-chain data. It provides a suite of tools and services to help you build, manage, and scale your Web3 applications. By leveraging enriched on-chain data and streaming computing technologies across one data infrastructure, ChainBase Data Platform automates the indexing and querying of blockchain data, enabling developers to accomplish complex data tasks with ease.

For more details, refer to the [ChainBase API Documentation](https://docs.chainbase.com/api-reference/overview).

## Author

This project was developed by **Harbhagwan Dhaliwal** (also known as Manpreet). Feel free to reach out or contribute to the project via GitHub.

GitHub Repository: [Link](https://github.com/HarbhagwanDhaliwal/Link/)

--- 