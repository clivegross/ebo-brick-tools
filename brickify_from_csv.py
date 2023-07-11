#!/usr/bin/python3
# File name: make_config_from_csv.py
# Description: Creates a Brick schema ttl file from a csv data file and config yml file.
# Used with brickify to construct a Brick Schema database from ttl files. Read:
# https://brickschema.readthedocs.io/en/latest/brickify/index.html.
# csv file expected with the following headers:
# Id,rdf_label,rdf_type,brick_hasLocation,brick_isFedBy,brick_hasUnit,brick_isPointOf,EBO_path
# Author: Clive Gross
# Last updated: 11-07-2023
import subprocess

# set the path to the equipment data csv here:
csv_file = "example/in_row_cooler_data.csv"
# set the config yaml file name here:
config_file = "example/equipment_model_in_row_cooler.yml"
# set the output ttl file  here:
output_file = "example/in_row_cooler_model.ttl"


def execute_command(command):
    """
    Execute shell command
    """
    try:
        print('Executing:', command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with return code {e.returncode}.\nError output:\n{e.output}")


def brickify_command(csv_file, output_file, config_file, input_type="csv"):
    """
    brickify EQUIPMENT_MODEL.csv --output equipment_model.ttl --input-type csv --config equipment_model.yml
    """
    command = f"brickify {csv_file} --output {output_file} --input-type {input_type} --config {config_file}"
    print(f"Brick model will be written to '{output_file}' if successful.")
    execute_command(command)
    print(f"Done. Check '{output_file}' for errors.")


if __name__ == '__main__':
    # Example usage
    brickify_command(csv_file, output_file, config_file)
    

