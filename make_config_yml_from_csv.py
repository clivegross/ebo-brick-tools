#!/usr/bin/python3
# File name: make_config_from_csv.py
# Description: Creates a config yml for brickify from a equipment point types csv.
# Used with brickify to construct a Brick Schema database from ttl files. Read:
# https://brickschema.readthedocs.io/en/latest/brickify/index.html.
# csv expected in the following format:
# bldg,rdfs:label,rdf:type,equipment_rdf:type,brick:hasLocation,brick:hasUnit,nsp:hasPath
# _SaTmpSp,Supply Air Temperature Setpoint,brick:Supply_Air_Temperature_Setpoint,brick:Computer_Room_Air_Conditioning,,unit:DEG_C,{EBO_path}/{Id}/Setpoints/SaTmpSp//Value
# _ZnTmpSp,Zone Air Temperature Setpoint,brick:Zone_Air_Humidity_Setpoint,brick:Computer_Room_Air_Conditioning,,unit:DEG_C,{EBO_path}/{Id}/Setpoints/ZnTmpSp//Value
# Author: Clive Gross
# Last updated: 11-07-2023
import csv
import yaml

# set the path to the equipment model points csv here:
csv_file = "in_row_cooler_model_points.csv"
# set the output config yaml file name here:
config_yaml_file = "equipment_model_in_row_cooler.yml"
# this yaml file contains boilerplate header yaml required in most configs
template_header_yaml_file = "equipment_template_header.yml"
# Update with the desired equipment rdf:type
equipment_rdf_type = "brick:Computer_Room_Air_Conditioning"


def make_config():
    data = []

    # Read the CSV file and store the data in a list of dictionaries
    with open(csv_file, "r", encoding="utf-8-sig") as file:
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
    make_config()
