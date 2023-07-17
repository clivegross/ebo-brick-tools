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
from make_config_yml_from_csv import make_config
from brickify_from_csv import brickify_command
import os

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

def build_model(equipment_model_points_csv_file, equipment_data_csv_file, equipment_rdf_type, output_file):
    config_file = os.path.splitext(equipment_model_points_csv_file)[0] + ".yml"
    make_config(equipment_model_points_csv_file, config_file, equipment_rdf_type)
    brickify_command(equipment_data_csv_file, output_file, config_file)


if __name__ == '__main__':
    # Example usage
    build_model(equipment_model_points_csv_file, equipment_data_csv_file, equipment_rdf_type, output_file)
    

