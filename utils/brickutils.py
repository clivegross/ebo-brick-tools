# from brickschema.namespaces import BRICK
# from brickschema.graph import Graph

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
import brickschema
from brickschema.merge import merge_type_cluster
from rdflib import Namespace

# both graphs must have the same namespace
# AND must have RDFS.label for all entities
BLDG = Namespace("http://example.org/building/")

def validate(g):
    valid, _, report = g.validate()
    if not valid:
        raise Exception(report)

g1 = brickschema.Graph().load_file("bldg1")
#validate(g1)

g2 = brickschema.Graph().load_file("bldg2")
#validate(g2)

G = merge_type_cluster(g1, g2, BLDG, similarity_threshold=0.1)
validate(G)
G.serialize("merged.ttl", format="ttl")