import csv
import os
import tempfile
from ebobricktools.utils.fileutils import filter_csv_by_column
import pandas as pd


def make_config(equipment_model_points_csv_file, config_yaml_file, equipment_rdf_type, multi_location=False, multi_fed=False, points_only=False):
    """
    Generate a configuration YAML file from a CSV file containing equipment model points.

    :param equipment_model_points_csv_file: Path to the input CSV file containing equipment model points.
    :param config_yaml_file: Path to the output YAML file to be generated.
    :param equipment_rdf_type: The RDF type of the equipment to filter the CSV data.
    :param multi_location: Boolean flag indicating whether to use a multi-location template.
    :param multi_fed: Boolean flag indicating whether to use a multi-fed template.

    The function reads the input CSV file, filters the data based on the specified RDF type,
    and generates a configuration YAML file using the appropriate template based on the
    multi_location and multi_fed flags.
    """
    # this yaml file contains boilerplate header yaml required in most configs
    template_header_standard_yaml_file = "equipment_template_header.yml"
    template_header_multi_location_yaml_file = "equipment_template_header_multiple_hasLocation.yml"
    template_header_multi_fed_yaml_file = "equipment_template_header_multiple_isFedBy.yml"
    template_header_points_only_yaml_file = "equipment_points_only_template_header.yml"

    if multi_location:
        template_header_yaml_file = template_header_multi_location_yaml_file
    elif multi_fed:
        template_header_yaml_file = template_header_multi_fed_yaml_file
    elif points_only:
        template_header_yaml_file = template_header_points_only_yaml_file
    else:
        template_header_yaml_file = template_header_standard_yaml_file

    data = []

    # Read the CSV file and store the data in a list of dictionaries
    with open(equipment_model_points_csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Convert the data into the desired YAML format
    output = ""

    count = 0  # Counter variable to track the number of rows added

    # Add template points from csv
    for row in data:
        if row['equipment_rdf:type'] == equipment_rdf_type:
            output += f"      bldg:{{Id}}{row['bldg']} rdfs:label \"{row['rdfs:label']}\" ;\n"
            if row['rdf:type']:
                output += f"        rdf:type \"{row['rdf:type']}\" ;\n"
            if row.get('brick:hasLocation'):
                output += f"        brick:hasLocation \"{row['brick:hasLocation']}\" ;\n"
            if row['brick:hasUnit']:
                output += f"        brick:hasUnit \"{row['brick:hasUnit']}\" ;\n"
            if row['nsp:hasPath']:
                output += f"        nsp:hasPath \"{row['nsp:hasPath']}\" ;\n"
            output += f"        brick:isPointOf bldg:{{Id}} .\n"
            count += 1

    # Read the template YAML file
    # Instead of this:
    # with open(template_header_yaml_file, "r") as template_file:

    # Try using the absolute path to the file
    template_header_yaml_file = os.path.join(os.path.dirname(__file__), template_header_yaml_file)
    print(f"template_header_yaml_file: {template_header_yaml_file}")
    with open(template_header_yaml_file, "r") as template_file:
        template_yaml = template_file.read()

    # Replace EQUIPMENT_TYPE with equipment_rdf_type
    template_yaml = template_yaml.replace("{{EQUIPMENT_TYPE}}", equipment_rdf_type)

    # Concatenate the template YAML with the converted CSV data
    final_yaml = template_yaml
    if count > 0:
        final_yaml += f"\n  -\n"
        final_yaml += f"    conditions:\n      - |\n"
        final_yaml += f"        '{{rdf_type}}' == \"{equipment_rdf_type}\"\n"
        final_yaml += f"    data: |-\n"
        final_yaml += output

    # Write the final YAML data to a file
    with open(config_yaml_file, "w") as file:
        file.write(final_yaml)

    print(f"Config '{config_yaml_file}' complete. {count} points added.")

def make_config_per_equipment_type(equipment_model_points_csv_file, equipment_types=None, output_config_yaml_file_prefix='', equipment_type_col='EQUIPMENT TYPE', equipment_rdf_type_col='equipment_rdf:type', multi_location=False, multi_fed=False):
    """
    Generate configuration YAML file/s from a CSV file containing equipment model points. One config file per equipment type. Returns a dictionary of equipment types and their corresponding config YAML file paths.

    :param equipment_model_points_csv_file: Path to the input CSV file containing equipment model points.
    :param equipment_types: List of equipment types to generate config YAML files for. If None, all unique equipment types in the model points CSV file will be used.
    :param output_config_yaml_file_prefix: Prefix for the output YAML file paths to be generated.
    :param equipment_type_col: Column name for equipment types in the CSV file.
    :param multi_location: Boolean flag indicating whether to use a multi-location template.
    :param multi_fed: Boolean flag indicating whether to use a multi-fed template.
    :return: Dictionary of equipment types and their corresponding config YAML file paths.
    """
    equipment_configs = {}

    # If equipment types are not provided, get all unique equipment types from the CSV file
    if equipment_types is None:
        # Read the CSV file
        data = []
        with open(equipment_model_points_csv_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        # Get unique equipment types
        # Get unique equipment types and their corresponding RDF types
        equipment_types = {row[equipment_type_col]: row[equipment_rdf_type_col] for row in data}

    # Generate config for each equipment type
    for idx, (equipment_type, equipment_rdf_type) in enumerate(equipment_types.items(), start=1):
         # Create a temporary CSV file for the current equipment type
        temp_csv_file_path = os.path.join(tempfile.gettempdir(), "temp_equipment_model_points.csv")
        filter_csv_by_column(equipment_model_points_csv_file, temp_csv_file_path, equipment_type_col, equipment_type)
        
        # Generate the config YAML file for the current equipment type
        output_config_yaml_file = f"{output_config_yaml_file_prefix}_{idx}.yml"
        make_config(temp_csv_file_path, output_config_yaml_file, equipment_rdf_type, multi_location, multi_fed)
        equipment_configs[equipment_type] = output_config_yaml_file

        # Remove the temporary CSV file
        os.remove(temp_csv_file_path)

    return equipment_configs


def get_equipment_types_from_csv(csv_file_path, equipment_type_col='EQUIPMENT TYPE', equipment_rdf_type_col='rdf_type'):
    """
    Get unique equipment types and their corresponding RDF types from a CSV file.

    :param csv_file_path: Path to the input CSV file.
    :param equipment_type_col: Column name for equipment types in the CSV file.
    :param equipment_rdf_type_col: Column name for RDF types in the CSV file.
    :return: Dictionary of equipment types and their corresponding RDF types, eg:
                {'Audio Visual Systems': 'brick:Audio_Visual_System'}
    """
    # Read the CSV file
    data = pd.read_csv(csv_file_path)

    # Get unique equipment types and their corresponding RDF types
    equipment_types = {row[equipment_type_col]: row[equipment_rdf_type_col] for _, row in data.iterrows()}

    return equipment_types



if __name__ == '__main__':
    # Example usage
    # set the path to the equipment model points csv here:
    equipment_model_points_csv_file = "example/in_row_cooler_model_points.csv"
    # set the output config yaml file name here:
    config_yaml_file = "example/in_row_cooler_model_points.yml"
    # Update with the desired equipment rdf:type
    equipment_rdf_type = "brick:Computer_Room_Air_Conditioning"
    # Make the config file
    make_config(equipment_model_points_csv_file, config_yaml_file, equipment_rdf_type)
