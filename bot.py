import discord
from discord import app_commands
from config import BOT_TOKEN, MAX_TABLE_SHOW
from apis.api_sql import execute_query_and_fetch_results
from utils import (split_message, get_table,
                   format_dataframe_table,
                   save_dataframe_as_image,
                   get_network_id,
                   format_data_for_discord,
                   generate_random_filename)
import json
import os
import io
import pandas as pd
from apis.api_web3 import (api_get_block_by_number,
                           api_get_transaction,
                           api_get_native_token_balance,
                           api_get_token_metadata,
                           api_get_token_price,
                           api_get_nft_metadata,
                           api_resolve_ens_domain
                           )


class MyClient(discord.Client):
    def __init__(self, *, bot_intents: discord.Intents):
        super().__init__(intents=bot_intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sync global commands
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(bot_intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await client.tree.sync()  # Ensure commands are synced globally


@client.tree.command(name="sql")
@app_commands.describe(query='Execute the SQL query to show up to 4 columns and 20 rows')
async def sql(interaction: discord.Interaction, query: str):
    """Executes an SQL query and returns the result."""
    followup = None
    total_columns = 0
    total_rows = 0
    try:
        # Defer the interaction
        await interaction.response.defer()
        # Send a follow-up message
        followup = await interaction.followup.send("Please wait...")

        # Process the query
        response = await execute_query_and_fetch_results(query)
        if response:
            response_json = json.dumps(response)
            if 'Data' in response_json:
                # Access columns and data
                columns = response['Columns']
                column_names = [item['name'] for item in columns]
                data = response['Data']
                (df, total_columns, total_rows) = get_table(column_names, data)
                table_image = save_dataframe_as_image(df)
                result_str = table_image  # Set result_str to the image file path
            else:
                result_str = response  # String result
        else:
            result_str = "Failed to retrieve API data."

        # Check if result_str is a file path or a string
        if type(result_str) is str and os.path.isfile(result_str):

            await followup.edit(content=(
                f"  :mag_right:  We found `{total_columns}` columns and `{total_rows}` rows."
                f" (preview below :arrow_down: )\n \n"
            ))

            # Read the file as bytes
            with open(result_str, 'rb') as file:
                file_bytes = file.read()

            # Send the image file as bytes
            discord_file = discord.File(fp=io.BytesIO(file_bytes), filename=os.path.basename(result_str))
            await interaction.followup.send(content=":bar_chart:  **Preview**:", file=discord_file)

            # Remove the temporary file after sending
            os.remove(result_str)
        else:
            # Use the split_message utility function
            result_str = str(result_str)
            chunks = split_message(result_str)

            await followup.edit(content=f'```{chunks[0]}```')

            # Send remaining chunks as follow-up messages
            chunk_count = 0
            for chunk in chunks[1:]:
                chunk_count += 1
                await interaction.followup.send(f'```{chunk}```')
                if chunk_count >= MAX_TABLE_SHOW:
                    break  # Check if result_str is a file path or a string

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="sql_excel")
@app_commands.describe(query='Execute the SQL query and get the result in an Excel file.')
async def sql_excel(interaction: discord.Interaction, query: str):
    """Executes an SQL query and sends the result as an Excel file."""
    followup = None
    try:
        # Defer the interaction
        await interaction.response.defer()
        # Send a follow-up message
        followup = await interaction.followup.send("Please wait...")

        # Process the query
        response = await execute_query_and_fetch_results(query)
        if response:
            response_json = json.dumps(response)
            if 'Data' in response_json:
                # Access columns and data
                columns = response['Columns']
                column_names = [item['name'] for item in columns]
                data = response['Data']

                # Prepare DataFrame for Excel file
                (df, total_columns, total_rows) = get_table(column_names, data, max_column=None,
                                                            max_row=None, hidden=False)

                # Send column and row information
                await followup.edit(content=(
                    f":mag_right:  We found `{total_columns}` columns and `{total_rows}` rows. "
                    f"(download below :arrow_down: )\n\n"
                ))

                # Generate a random filename
                filename = generate_random_filename()

                # Convert DataFrame to Excel
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Sheet1', index=False)
                excel_buffer.seek(0)

                # Create a Discord file
                discord_file = discord.File(fp=excel_buffer, filename=filename)
                await interaction.followup.send(content=":inbox_tray:  **Download**:", file=discord_file)

                # Cleanup: Close buffer
                excel_buffer.close()

            else:
                result_str = response  # String result

                await followup.edit(content=f'```{result_str}```')

        else:
            await followup.edit(content="Failed to retrieve API data.")

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_block_by_number")
@app_commands.describe(number='Block number to fetch', chain='Chain ID or Name')
async def get_block_by_number(interaction: discord.Interaction, number: str, chain: str):
    """Fetches block details by block number and chain ID."""
    followup = None
    try:
        # Defer the interaction
        await interaction.response.defer()
        # Send a follow-up message
        followup = await interaction.followup.send("Please wait...")

        # Fetch block details
        response = await api_get_block_by_number(number, get_network_id(chain))
        if response:
            response_json = json.dumps(response)
            if 'data' in response_json and response['data'] is not None and response['data'] != "null":
                data = response['data']

                # Extracting columns and data from the 'data' key
                columns = list(data.keys())
                data = list(data.values())

                # table_image = save_dataframe_as_image(df)
                result_str = format_data_for_discord(columns, data)
            else:
                result_str = response  # String result
        else:
            result_str = "Failed to retrieve API data."

        # Use the split_message utility function
        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        # Send remaining chunks as follow-up messages
        chunk_count = 0
        for chunk in chunks[1:]:
            chunk_count += 1
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')
            if chunk_count >= MAX_TABLE_SHOW:
                break

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_transaction")
@app_commands.describe(tx_hash='Transaction hash', chain='Chain ID or Name',
                       block_number='Block number', tx_index='Transaction index')
async def get_transaction(interaction: discord.Interaction, tx_hash: str, chain: str,
                          block_number: str = None, tx_index: str = None):
    """Get the detail of a transaction given the transaction hash"""
    followup = None
    try:
        await interaction.response.defer()
        followup = await interaction.followup.send("Please wait...")

        response = await api_get_transaction(tx_hash, get_network_id(chain), block_number, tx_index)
        if response:
            if 'data' in response and response['data'] is not None and response['data'] != "null":
                data = response['data']
                columns = list(data.keys())
                data_values = list(data.values())
                result_str = format_data_for_discord(columns, data_values)
            else:
                result_str = response
        else:
            result_str = "Failed to retrieve API data."

        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        for chunk in chunks[1:]:
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_native_token_balance")
@app_commands.describe(address='Address to fetch balance', chain='Chain ID or Name', block='Block number or "latest"')
async def get_native_token_balance(interaction: discord.Interaction, address: str, chain: str, block: str = "latest"):
    """Get the native token balance for a specified address"""
    followup = None
    try:
        await interaction.response.defer()
        followup = await interaction.followup.send("Please wait...")

        response = await api_get_native_token_balance(address, get_network_id(chain), block)
        if response:
            if 'data' in response and response['data'] is not None and response['data'] != "null":
                data = response['data']
                result_str = format_data_for_discord(["Data"], [data])
            else:
                result_str = response
        else:
            result_str = "Failed to retrieve API data."

        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        for chunk in chunks[1:]:
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_token_metadata")
@app_commands.describe(contract_address='Token contract address', chain='Chain ID or Name')
async def get_token_metadata(interaction: discord.Interaction, contract_address: str, chain: str):
    """Get the metadata of a specified token"""
    followup = None
    try:
        await interaction.response.defer()
        followup = await interaction.followup.send("Please wait...")

        response = await api_get_token_metadata(contract_address, get_network_id(chain))
        if response:
            if 'data' in response and response['data'] is not None and response['data'] != "null":
                data = response['data']
                columns = list(data.keys())
                data_values = list(data.values())
                result_str = format_data_for_discord(columns, data_values, max_length=500, stars_count=0)
            else:
                result_str = response
        else:
            result_str = "Failed to retrieve API data."

        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        for chunk in chunks[1:]:
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_token_price")
@app_commands.describe(contract_address='Token contract address', chain='Chain ID or Name')
async def get_token_price(interaction: discord.Interaction, contract_address: str, chain: str):
    """Get the price of a specified token"""
    followup = None
    try:
        await interaction.response.defer()
        followup = await interaction.followup.send("Please wait...")

        response = await api_get_token_price(contract_address, get_network_id(chain))
        if response:
            if 'data' in response and response['data'] is not None and response['data'] != "null":
                data = response['data']
                columns = list(data.keys())
                data_values = list(data.values())
                result_str = format_data_for_discord(columns, data_values, max_length=100, stars_count=0)
            else:
                result_str = response
        else:
            result_str = "Failed to retrieve API data."

        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        for chunk in chunks[1:]:
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_nft_metadata")
@app_commands.describe(contract_address='NFT contract address', nft_id='NFT token ID', chain='Chain ID or Name')
async def get_nft_metadata(interaction: discord.Interaction, contract_address: str, nft_id: str, chain: str):
    """Get the metadata associated with the specified NFT"""
    followup = None
    try:
        await interaction.response.defer()
        followup = await interaction.followup.send("Please wait...")

        response = await api_get_nft_metadata(contract_address, nft_id, get_network_id(chain))
        if response:
            if 'data' in response and response['data'] is not None and response['data'] != "null":
                data = response['data']
                columns = list(data.keys())
                data_values = list(data.values())
                result_str = format_data_for_discord(columns, data_values, max_length=500, stars_count=0)
            else:
                result_str = response
        else:
            result_str = "Failed to retrieve API data."

        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        for chunk in chunks[1:]:
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="get_domain_metadata")
@app_commands.describe(domain='ENS domain to resolve', chain='Chain ID or Name', block='Block number or "latest"')
async def resolve_ens_domain(interaction: discord.Interaction, domain: str, chain: str, block: str = "latest"):
    """Resolve an ENS domain to its associated address"""
    followup = None
    try:
        await interaction.response.defer()
        followup = await interaction.followup.send("Please wait...")

        response = await api_resolve_ens_domain(domain, get_network_id(chain), block)
        if response:
            if 'data' in response and response['data'] is not None and response['data'] != "null":
                data = response['data']
                columns = list(data.keys())
                data_values = list(data.values())
                result_str = format_data_for_discord(columns, data_values, max_length=200, stars_count=0)
            else:
                result_str = response
        else:
            result_str = "Failed to retrieve API data."

        result_str = str(result_str)
        chunks = split_message(result_str)

        if response and 'data' in response and response['code'] == 200:
            followup = await followup.edit(content=f':bar_chart:  **Table Preview**: ```{chunks[0]}```')
        else:
            followup = await followup.edit(content=f'```{chunks[0]}```')

        for chunk in chunks[1:]:
            await interaction.followup.send(f':bar_chart:  **Preview**: ```{chunk}```')

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="help")
async def help_command(interaction: discord.Interaction):
    """Provides information about available commands."""
    commands_info = [
        {"name": "/sql", "description": "Execute the SQL query to show up to 4 columns and 20 rows."},
        {"name": "/sql_excel", "description": "Execute the SQL query and get the result in an Excel file."},
        {"name": "/get_block_by_number", "description": "Fetch block details by block number and chain ID."},
        {"name": "/get_transaction", "description": "Get the details of a transaction given the transaction hash."},
        {"name": "/get_native_token_balance", "description": "Get the native token balance for a specified address."},
        {"name": "/get_token_metadata", "description": "Get the metadata of a specified token."},
        {"name": "/get_token_price", "description": "Get the price of a specified token."},
        {"name": "/get_nft_metadata", "description": "Get the metadata associated with the specified NFT."},
        {"name": "/get_domain_metadata", "description": "Resolve an ENS domain to its associated address."},
    ]

    help_text = "**Available Commands:**\n\n"
    for command in commands_info:
        help_text += f"**{command['name']}**: {command['description']}\n\n"

    await interaction.response.send_message(help_text)


def run_bot():
    client.run(BOT_TOKEN)
