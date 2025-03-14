import pandas as pd

def read_excel_filter_and_write_to_csv(input_excel_path, output_csv_path, sheet_name=0, filter_column=None, filter_value=None, columns_to_include=None, filters=None):
    """
    Reads an Excel file, optionally filters rows based on a column value, optionally includes only specified columns,
    and writes the result to a CSV file.

    :param input_excel_path: Path to the input Excel file.
    :param output_csv_path: Path to the output CSV file.
    :param sheet_name: Name or index of the sheet to read.
    :param filter_column: For single column/value filter, column name to filter rows by.
    :param filter_value: For single column/value filter, value(s) to filter rows by (can be a single value or a list).
    :param columns_to_include: List of column names to include in the output CSV.
    :param filters: For multiple column/value filters, list of tuples where each tuple contains a column name and a value to filter rows by.
    # Example usage
    filters = [('SYSTEM', 'Audio Visual Systems')]
    read_excel_filter_and_write_to_csv(
        'path/to/input.xlsx',
        'path/to/output.csv',
        sheet_name='Sheet1',
        filters=filters,
        columns_to_include=['Id', 'rdf_label', 'rdf_type', 'brick_hasLocation', 'brick_feeds', 'brick_isPartOf', 'brick_isFedBy', 'EBO_path']
    )
    """
    # Read the Excel file
    df = pd.read_excel(input_excel_path, sheet_name=sheet_name)

    # Filter rows if filter_column and filter_value are provided
    if filter_column and filter_value is not None:
        if isinstance(filter_value, list):
            df = df[df[filter_column].isin(filter_value)]  # Handle multiple values
        else:
            df = df[df[filter_column] == filter_value]  # Handle single value

    # Apply filters
    if filters:
        for column, value in filters:
            if isinstance(value, list):
                df = df[df[column].isin(value)]
            else:
                df = df[df[column] == value]

    # Include only specified columns if columns_to_include is provided
    if columns_to_include:
        df = df[columns_to_include]

    # Write the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)

# Example usage
# read_excel_filter_and_write_to_csv('input.xlsx', 'output.csv', sheet_name='Sheet1', filter_column='Status', filter_value='Active', columns_to_include=['Name', 'Age'])