import codecs

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


if __name__ == '__main__':
    # Example usage
    file_path = "example_file.txt"
    check_and_convert_utf8(file_path)

