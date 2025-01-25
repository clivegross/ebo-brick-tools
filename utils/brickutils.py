from brickschema.namespaces import BRICK
from brickschema.graph import Graph

# def combine_ttl_files(input_files, output_file):
#     combined_data = ""
#     # Read data from each input file and combine
#     for file in input_files:
#         with open(file, 'r') as f:
#             combined_data += f.read()
#     # Create a new graph
#     graph = Graph()
#     # Load the combined data into the graph
#     graph.load_rdf(combined_data, format="ttl")
#     # Validate the graph against the Brick schema
#     validation_result = graph.validate()
#     if validation_result:
#         print("Validation successful!")
#     else:
#         print("Validation failed!")
#     # Write the combined data to the output file
#     with open(output_file, 'w') as f:
#         f.write(combined_data)
#     print("Files combined successfully!")

# Example usage
# input_files = ["file1.ttl", "file2.ttl", "file3.ttl"]
# output_file = "combined.ttl"
# combine_ttl_files(input_files, output_file)

# https://brickschema.readthedocs.io/en/latest/merging.html
import os
import brickschema
from brickschema.merge import merge_type_cluster
from rdflib import Namespace

# both graphs must have the same namespace
# AND must have RDFS.label for all entities
BLDG = Namespace("http://example.org/building/")

def validate(g):
    if isinstance(g, str):
        g = brickschema.Graph().load_file(g)
    valid, _, report = g.validate()
    if not valid:
        raise Exception(report)
    return (valid, report)
    
def file_to_model(input_file):
    return brickschema.Graph().load_file(input_file)
    
def model_to_file(g, output_file, format="ttl"):
    g.serialize(output_file, format=format)
    
def merge_models(
        f1, # input file 1
        f2, # input file 2
        output_file="merged.ttl",
        format="ttl",
        BLDG=Namespace("http://example.org/building/"),
        similarity_threshold=0.1,
        delete_old_files=False,
        validate=True
    ):
    # load the model files into the graph and validate
    print(f'loading {f1} into graph...')
    g1 = brickschema.Graph().load_file(f1)
    if validate:
        print(f'validating {f1}...')
        validate(g1)
    print(f'loading {f2} into graph...')
    g2 = brickschema.Graph().load_file(f2)
    if validate:
        print(f'validating {f2}...')
        validate(g2)
    # merge the models and validate
    print("Merging models...")
    G = merge_type_cluster(g1, g2, BLDG, similarity_threshold=similarity_threshold)
    if validate:
        print("Merged model created, validating...")
        validate(G)
        print("Validation successful!")
    # write the merged model to a file
    print(f"Writing merged model to {output_file}...")
    G.serialize(output_file, format=format)
    print(f"Model written to {output_file} successfully!")
    # delete the old files if required
    if delete_old_files:
        print("Deleting old files...")
        os.remove(f1)
        os.remove(f2)
        print("Old files deleted successfully!")

def dirty_append_models(
        f1, # input file 1
        f2, # input file 2
        output_file="merged.ttl",
    ):
    '''
    Use this to reduce merge time when you know the data is good and there is know complex joining required, just appending.
    Skip the first @prefix declarations and blank row from the second input file, then just append everything else to the end of the first file and write to output_file.
    ```
    @prefix bldg: <https://example.com/bldg#> .
    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix nsp: <https://w3id.org/se/building/nsp#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    ```
    '''
    def filter_lines(lines):
        return [line for line in lines if not line.strip().startswith("@prefix") and line.strip()]

    # Read the first file
    with open(f1, 'r') as f:
        data1 = f.readlines()

    # Read the second file and filter lines
    with open(f2, 'r') as f:
        data2 = f.readlines()
        filtered_data2 = filter_lines(data2)

    # Write to the output file
    with open(output_file, 'w') as f:
        f.writelines(data1)
        f.writelines(filtered_data2)

    print(f"Appended {f2} to {f1} and wrote to {output_file} successfully!")

# g1 = brickschema.Graph().load_file("bldg1")
# #validate(g1)

# g2 = brickschema.Graph().load_file("bldg2")
# #validate(g2)

# G = merge_type_cluster(g1, g2, BLDG, similarity_threshold=0.1)
# validate(G)
# G.serialize("merged.ttl", format="ttl")