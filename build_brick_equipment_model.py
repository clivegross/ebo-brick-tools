#!/usr/bin/python3
# File name: build_brick_equipment_model.py
# Description: Combines functionality of make_config_yml_from_csv.py and brickify_from_csv.py to 
# build a brick model given a csv continaing
# Used with brickify to construct a Brick Schema database from ttl files. Read:
# https://brickschema.readthedocs.io/en/latest/brickify/index.html.
# csv file expected with the following headers:
# Id,rdf_label,rdf_type,brick_hasLocation,brick_isFedBy,brick_hasUnit,brick_isPointOf,EBO_path
# Author: Clive Gross
# Last updated: 11-07-2023
from .utils.fileutils import filter_csv_by_column
from .make_config_yml_from_csv import make_config
from .brickify_from_csv import brickify_command
from .make_config_yml_from_csv import make_config_per_equipment_type
from .utils.brickutils import dirty_append_models, merge_models, file_to_model, model_to_file
import os
import tempfile
import csv


def build_model(equipment_model_points_csv_file, equipment_data_csv_file, equipment_rdf_type, output_file, multi_location=False, multi_fed=False):
    config_file = os.path.splitext(equipment_model_points_csv_file)[0] + ".yml"
    make_config(equipment_model_points_csv_file, config_file, equipment_rdf_type, multi_location=multi_location, multi_fed=multi_fed)
    brickify_command(equipment_data_csv_file, output_file, config_file)


def build_model_per_equipment_type(equipment_data_csv_file, equipment_configs, equipment_type_col, output_file_prefix):
    """
    Run brickify_command for each equipment type using the provided equipment_configs dictionary.

    :param equipment_data_csv_file: Path to the input CSV file containing equipment data.
    :param equipment_configs: Dictionary of equipment types and their corresponding config YAML file paths.
    :param equipment_type_col: Column name for equipment types in the CSV file.
    :param output_file_prefix: The prefix including the full path to the output TTL files. eg ./outputs/av will create ./outputs/av_1.ttl, ./outputs/av_2.ttl, etc. for each equipment type.
    """
    # Read the CSV file
    output_models = []

    # Run brickify_command for each equipment type
    for idx, (equipment_type, config_file) in enumerate(equipment_configs.items(), start=1):

        # Create a temporary CSV file for the current equipment type
        temp_csv_file_path = os.path.join(tempfile.gettempdir(), "temp_filtered_equipment_data.csv")
        filter_csv_by_column(equipment_data_csv_file, temp_csv_file_path, equipment_type_col, equipment_type)
        print(f"\nRunning brickify for {equipment_type} using {config_file}...")
        # Generate the config YAML file for the current equipment type
        output_file = f"{output_file_prefix}_{idx}.ttl"

        # Run the brickify_command
        brickify_command(temp_csv_file_path, output_file, config_file)
        output_models.append(output_file)

        # Remove the temporary CSV file
        os.remove(temp_csv_file_path)

    return output_models


def validate_and_merge_models(models, output_file, delete_old_files=True, validate=True, dirty=False):
    # map temporary output file for each equipment type
    number_of_models_to_merge = len(models)
    print(f"Number of models to merge: {number_of_models_to_merge}")
    for idx, model in enumerate(models):
        # first copy the first model to the output file
        if idx == 0:
            print(f"Copying {model} to {output_file}")
            g0 = file_to_model(model)
            model_to_file(g0, output_file)
        # then merge the rest one by one into the output file
        if idx > 0:
            try:
                # every model except the first one
                print(f"Merging {model} with {output_file}")
                if dirty:
                    dirty_append_models(output_file, model, output_file)
                else:
                    merge_models(model, output_file, output_file, format="ttl", validate=validate)
                # delete individual model files after merging into federated model
                if delete_old_files:
                    print(f"Removing {model}")
                    os.remove(model)
            except Exception as e:
                print(f"Error merging {model} with {output_file}: {e}")


if __name__ == '__main__':
    # set the path to the equipment model points csv here:
    equipment_model_points_csv_file = "example/in_row_cooler_model_points.csv"
    # Update with the desired equipment class rdf:type
    equipment_rdf_type = "brick:Computer_Room_Air_Conditioning"
    # set the path to the equipment data csv here:
    equipment_data_csv_file = "example/in_row_cooler_data.csv"
    # Uncomment this line to convert a UTF-8 with BOM encoded data csv to UTF-8 before running brickify (brickify cant handle non-UTF-8 encoded csv)
    # equipment_data_csv_file = "example/in_row_cooler_data_utf8_bom.csv"
    # set the output ttl filename here:
    output_file = "example/in_row_cooler_model.ttl"
    # Example usage
    build_model(equipment_model_points_csv_file, equipment_data_csv_file, equipment_rdf_type, output_file)
    
    # Example usage
    equipment_model_points_csv_file = "example/in_row_cooler_model_points.csv"
    output_config_yaml_file_prefix = "example/config"
    equipment_configs = make_config_per_equipment_type(equipment_model_points_csv_file, output_config_yaml_file_prefix)

    equipment_data_csv_file = "example/equipment_data.csv"
    build_model_per_equipment_type(equipment_configs, 'EQUIPMENT TYPE', equipment_data_csv_file)

