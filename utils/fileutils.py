import codecs
import pandas as pd

def check_and_convert_utf8(file_path):
    BOMS = [
        (codecs.BOM_UTF32, 'utf-32'),
        (codecs.BOM_UTF16, 'utf-16'),
        (codecs.BOM_UTF8, 'utf-8-sig')
    ]

    with open(file_path, 'rb') as file:
        raw_data = file.read(4)

    for bom, encoding in BOMS:
        if raw_data.startswith(bom):
            content = open(file_path, 'r', encoding=encoding).read()
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"File '{file_path}' converted from {encoding} to UTF-8.")
            return

    print(f"File '{file_path}' is already encoded as UTF-8.")

def filter_csv_by_column(input_csv_path, output_csv_path, filter_column, filter_value):
    """
    Load a CSV file, filter by a column value, and write to an output file.

    :param input_csv_path: Path to the input CSV file.
    :param output_csv_path: Path to the output CSV file.
    :param filter_column: Column name to filter by.
    :param filter_value: Value to filter the column by.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path)

    # Filter the DataFrame by the specified column and value
    filtered_df = df[df[filter_column] == filter_value]

    # Write the filtered DataFrame to the output CSV file
    filtered_df.to_csv(output_csv_path, index=False)




if __name__ == '__main__':
    # Example usage
    file_path = "example_file.txt"
    check_and_convert_utf8(file_path)

    # Example usage
    input_csv_path = 'path/to/input.csv'
    output_csv_path = 'path/to/output.csv'
    filter_column = 'EQUIPMENT TYPE'
    filter_value = 'Audio Visual Systems'

    filter_csv_by_column(input_csv_path, output_csv_path, filter_column, filter_value)
