---

# Link Discord Bot

We have developed **Link**, a Discord bot that connects with the Chainbase Network. It's an open-source project that anyone can use.

## What is Chainbase Data Platform?

Chainbase Data Platform is an all-in-one data infrastructure for Web3 that allows you to index, transform, and utilize large-scale on-chain data. It provides a suite of tools and services to help you build, manage, and scale your Web3 applications. By leveraging enriched on-chain data and streaming computing technologies across one data infrastructure, Chainbase Data Platform automates the indexing and querying of blockchain data, enabling developers to accomplish complex data tasks with ease.

For more details, refer to the [Chainbase API Documentation](https://docs.chainbase.com/api-reference/overview).

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
- **/help**: Provides information about available commands.

## Setup and Installation

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/HarbhagwanDhaliwal/Link.git
cd Link
```

## Step 2: Get the API Key and Discord Token

You will need API key and Discord Token to run this bot:

1. **Chainbase API Key**: Used to fetch data from Chainbase.  
   - [Create a Chainbase account and get your API key](https://console.chainbase.com/).

2. **Discord Token**: Required to interact with Discord.  
   - [Create a Discord application and get your Token](https://discord.com/developers/applications).


### Step 3: Set Environment Variables

Set up the following environment variables in your system:

```bash
export DISCORD_BOT_TOKEN=your_discord_bot_token
export CHAINBASE_SQL_BASE_URL=https://api.chainbase.com/api/v1
export CHAINBASE_WEB3_BASE_URL=https://api.chainbase.online/v1
export CHAINBASE_API_KEY=your_chainbase_api_key
export FLOCK_AUTH_TOKEN=your_flock_model_api_key
```

You can obtain the Chainbase API key from the Chainbase console. For the Discord bot token, create a Discord application and generate the token from there.

### Step 4: Install Dependencies

Install the required Python dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 5: Run the Bot

After setting up the environment variables and installing dependencies, run the bot using:

```bash
python3 main.py
```
## Running as a System Service on Ubuntu

To ensure that your Python script (`main.py`) runs continuously as a system service, follow the steps below:

### 1. Create a Service File
Create a new service file for your project by running the following command:

```bash
sudo nano /etc/systemd/system/my_discord_bot.service
```
Add the following content to the file:

```bash
[Unit]
Description=Link Discord Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Link
ExecStart=/usr/bin/python3 /root/Link/main.py
Environment="DISCORD_BOT_TOKEN=your_discord_bot_token"
Environment="CHAINBASE_SQL_BASE_URL=https://api.chainbase.com/api/v1"
Environment="CHAINBASE_WEB3_BASE_URL=https://api.chainbase.online/v1"
Environment="CHAINBASE_API_KEY=your_chainbase_api_key"
Restart=on-failure

[Install]
WantedBy=multi-user.target


```
Replace `root` with your Ubuntu username.
Replace `/root/Link` with the actual path to your project directory.

### 2. Reload `systemd` to Apply the New Service

```bash
sudo systemctl daemon-reload
```

### 3. Start the Service

```bash
sudo systemctl start my_discord_bot.service
```

### 4. Enable the Service to Start on Boot

```bash
sudo systemctl enable my_discord_bot.service
```

### 5. Check the Status of the Service

```bash
sudo systemctl status my_discord_bot.service
```

## Author

This project was developed by **Harbhagwan Dhaliwal** (also known as Manpreet). Feel free to reach out or contribute to the project via GitHub.

GitHub Repository: [Link](https://github.com/HarbhagwanDhaliwal/Link/)

--- 
