import csv
import yaml


def make_config(equipment_model_points_csv_file, config_yaml_file, equipment_rdf_type):
    # this yaml file contains boilerplate header yaml required in most configs
    template_header_yaml_file = "equipment_template_header.yml"

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
            if row['brick:hasLocation']:
                output += f"        brick:hasLocation \"{row['brick:hasLocation']}\" ;\n"
            if row['brick:hasUnit']:
                output += f"        brick:hasUnit \"{row['brick:hasUnit']}\" ;\n"
            if row['nsp:hasPath']:
                output += f"        nsp:hasPath \"{row['nsp:hasPath']}\" ;\n"
            output += f"        brick:isPointOf bldg:{{Id}} .\n"
            count += 1

    # Read the template YAML file
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
