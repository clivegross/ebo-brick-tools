import pandas as pd

def read_excel_filter_and_write_to_csv(input_excel_path, output_csv_path, sheet_name=0, filter_column=None, filter_value=None, columns_to_include=None):
    """
    Reads an Excel file, optionally filters rows based on a column value, optionally includes only specified columns,
    and writes the result to a CSV file.

    :param input_excel_path: Path to the input Excel file.
    :param output_csv_path: Path to the output CSV file.
    :param sheet_name: Name or index of the sheet to read.
    :param filter_column: Column name to filter rows by.
    :param filter_value: Value to filter rows by.
    :param columns_to_include: List of column names to include in the output CSV.
    """
    # Read the Excel file
    df = pd.read_excel(input_excel_path, sheet_name=sheet_name)

    # Filter rows if filter_column and filter_value are provided
    if filter_column and filter_value is not None:
        df = df[df[filter_column] == filter_value]

    # Include only specified columns if columns_to_include is provided
    if columns_to_include:
        df = df[columns_to_include]

    # Write the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)

# Example usage
# read_excel_filter_and_write_to_csv('input.xlsx', 'output.csv', sheet_name='Sheet1', filter_column='Status', filter_value='Active', columns_to_include=['Name', 'Age'])