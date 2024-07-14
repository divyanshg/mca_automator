import pandas as pd
from datetime import datetime, timedelta

def filter_xlsx(xlsx_file):
    """
    Load data from an XLSX file and filter rows based on the 'DATE OF INCORPORATION' column.

    Parameters:
    xlsx_file (str): The path to the XLSX file.

    Returns:
    DataFrame: A DataFrame containing the filtered rows.
    """
    print(f"Using file: {xlsx_file}")
    df = pd.read_excel(xlsx_file, header=1)
    yesterday = (datetime.now() - timedelta(1)).strftime('%d-%b-%Y').upper()
    # print(yesterday)
    filtered_df = df[df['DATE OF INCORPORATION'] == yesterday]
    print(len(filtered_df))
    return filtered_df
