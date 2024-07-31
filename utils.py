from tabulate import tabulate
import pandas as pd
from config import MAX_COLUMN_SHOW, MAX_ROW_SHOW
import matplotlib.pyplot as plt
import uuid
import os
import tempfile
import random
import io
import string


def format_as_table(columns, data):
    """Formats the query result as a table."""
    headers = [col['name'] for col in columns]
    table = tabulate(data, headers=headers, tablefmt="pretty")
    return table


def format_dataframe_table(df):
    # Convert the DataFrame to a text-based table
    table_str = tabulate(df, headers='keys', tablefmt='grid')
    return table_str


def format_table(columns, data):
    """Convert columns and data into a tabular format string wrapped in code blocks."""
    # Create the header row
    header = " | ".join(columns)
    # Create a separator row
    separator = "-|-".join(["-" * len(col) for col in columns])
    # Create the data rows
    rows = []
    for row in data:
        rows.append(" | ".join(str(item) for item in row))

    # Combine header, separator, and rows into the final table string
    table = f"```\n{header}\n{separator}\n" + "\n".join(rows) + "\n```"

    return table


def truncate_text(text, max_length=15, stars_count=10):
    """Truncate text to the last part of max_length and
    add 'stars_count' stars at the beginning if it exceeds max_length."""
    text = str(text)  # Ensure the text is a string
    if len(text) > max_length:
        truncated_text = text[-max_length:]  # Get the last part of the text
        return '*' * stars_count + truncated_text  # Prepend stars
    return text


def get_table(columns, data, max_column=MAX_COLUMN_SHOW, max_row=MAX_ROW_SHOW, hidden=True):
    """
    Create a DataFrame from data, limiting the number of columns and rows.

    Parameters:
    - columns: List of column names.
    - data: List of rows, where each row is a list of values.
    - max_column: Maximum number of columns to display.
    - max_row: Maximum number of rows to display.

    Returns:
    - DataFrame with limited rows and columns.
    """
    # Create a DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Limit the number of columns to the first `max_column` columns
    df = df.iloc[:, :max_column]

    # Limit the number of rows to the first `max_row` rows
    df = df.head(max_row)

    # Truncate each cell in the DataFrame
    if hidden:
        df = df.apply(lambda col: col.map(lambda x: truncate_text(str(x))))

    return df


def save_dataframe_as_image(df, file_name=None, figsize=(10, 2), file_extension='png'):
    """
    Save a DataFrame as an image file with a specified name or a randomly generated name in a temp directory.

    Parameters:
    - df (pd.DataFrame): The DataFrame to save as an image.
    - file_name (str): The name of the file to save. If None, a random name will be generated.
    - figsize (tuple): Size of the figure (width, height).
    - file_extension (str): File extension for the image file (e.g., 'png', 'jpg').

    Returns:
    - str: The full path of the saved image file.
    """

    # Create a temporary directory
    temp_dir = tempfile.gettempdir()

    # Use the specified file name or generate a random one
    if file_name is None:
        file_name = str(uuid.uuid4()) + f'.{file_extension}'
    else:
        # Ensure file name has the correct extension
        if not file_name.lower().endswith(f'.{file_extension}'):
            file_name += f'.{file_extension}'

    file_path = os.path.join(temp_dir, file_name)

    # Create a plot of the dataframe
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values,
             colLabels=df.columns,
             cellLoc='center',
             loc='center')

    # Save the plot as an image with the specified or random name
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)  # Close the figure to avoid memory leaks

    return file_path


def split_message(content, limit=1900):
    """Splits a message into chunks of a specified limit."""
    return [content[i:i + limit] for i in range(0, len(content), limit)]


def generate_random_filename(extension=".xlsx"):
    """Generate a random filename with the given extension."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + extension
