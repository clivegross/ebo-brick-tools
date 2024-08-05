import pandas as pd

def read_excel_filter_and_write_to_csv(excel_path, table_name=None, sheet_name=None, filter_column=None, filter_value=None, csv_path='filtered_data.csv'):
    """
    Reads an Excel workbook, filters data by a matching column, and writes the result to a CSV file.

    :param excel_path: Path to the Excel file.
    :param table_name: Name of the table to read. If None, sheet_name must be provided.
    :param sheet_name: Name of the sheet to read. Used if table_name is None.
    :param filter_column: Column name to filter by.
    :param filter_value: Value to filter by in the filter_column.
    :param csv_path: Path to save the filtered data as a CSV file.
    """
    # Load the Excel file
    if table_name:
        # If table_name is provided, use it to read the specific table
        df = pd.read_excel(excel_path, table_name=table_name)
    elif sheet_name:
        # If sheet_name is provided, use it to read the specific sheet
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    else:
        raise ValueError("Either table_name or sheet_name must be provided.")

    # Filter the DataFrame if filter_column and filter_value are provided
    if filter_column and filter_value is not None:
        filtered_df = df[df[filter_column] == filter_value]
    else:
        filtered_df = df

    # Write the filtered DataFrame to a CSV file
    filtered_df.to_csv(csv_path, index=False)