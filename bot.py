import discord
from discord import app_commands
from config import BOT_TOKEN, MAX_TABLE_SHOW
from apis.api_sql import execute_query_and_fetch_results
from utils import split_message, get_table, format_dataframe_table, save_dataframe_as_image, generate_random_filename
import json
import os
import io
import pandas as pd


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


@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command(name="sql")
@app_commands.describe(query='The SQL query you want to execute')
async def sql(interaction: discord.Interaction, query: str):
    """Executes an SQL query and returns the result."""
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
                df = get_table(column_names, data)
                table_image = save_dataframe_as_image(df)
                result_str = table_image  # Set result_str to the image file path
            else:
                result_str = response  # String result
        else:
            result_str = "Failed to retrieve API data."

        # Check if result_str is a file path or a string
        if type(result_str) is str and os.path.isfile(result_str):
            await followup.edit(content=(
                "Due to Discord limits, we show only the first 4 columns and max 20 rows.\n\n"
                "Use a `SELECT` SQL query to choose specific columns.\n\n"
            ))

            # Read the file as bytes
            with open(result_str, 'rb') as file:
                file_bytes = file.read()

            # Send the image file as bytes
            discord_file = discord.File(fp=io.BytesIO(file_bytes), filename=os.path.basename(result_str))
            await interaction.followup.send(file=discord_file)

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
                    break

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


@client.tree.command(name="sql_excel")
@app_commands.describe(query='The SQL query you want to execute')
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
                df = get_table(column_names, data, max_column=100, max_row=1000, hidden=False)

                # Generate a random filename
                filename = generate_random_filename()
                print("filename: ", filename)

                # Convert DataFrame to Excel
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Sheet1', index=False)
                excel_buffer.seek(0)

                # Create a Discord file
                discord_file = discord.File(fp=excel_buffer, filename=filename)
                await interaction.followup.send(file=discord_file)

                # Cleanup: Close buffer and delete file
                excel_buffer.close()

            else:
                result_str = response  # String result
                await followup.edit(content=f"Query result: {result_str}")

        else:
            await followup.edit(content="Failed to retrieve API data.")

    except Exception as e:
        if followup:
            await followup.edit(content=f'An error occurred: {e}')
        else:
            await interaction.followup.send(content=f'An error occurred: {e}', ephemeral=True)


def run_bot():
    client.run(BOT_TOKEN)
