from brickschema.namespaces import BRICK
from brickschema.graph import Graph
from importlib.resources import files
import os
import brickschema
from brickschema.merge import merge_type_cluster
from rdflib import Namespace
# https://brickschema.readthedocs.io/en/latest/merging.html

# both graphs must have the same namespace
# AND must have RDFS.label for all entities
BLDG = Namespace("http://example.org/building/")
NSP = files(__package__).joinpath("nsp.ttl")

def validate(g):
    # Initialize the Brick graph
    graph = brickschema.Graph()
    print(f"Loading {NSP} into graph...")
    graph.load_file(NSP)
    if isinstance(g, str):
        print(f"Loading {g} into graph...")
        graph.load_file(g)
    else:
        print("Merging provided graph into the namespace graph...")
        graph += g
    print("Validating graph...")
    valid, _, report = graph.validate()
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
    f1,  # input file 1
    f2,  # input file 2
    output_file="merged.ttl",
):
    """
    Appends two TTL files, ensuring all unique @prefix declarations from both files 
    are included at the top of the merged file. Skips duplicate @prefix lines and 
    blank rows from the second file during the merge.

    Args:
        f1 (str): Path to the first TTL file.
        f2 (str): Path to the second TTL file.
        output_file (str): Path to the output merged TTL file.

    Example:
        Input TTLs:
        @prefix bldg: <https://example.com/bldg#> .
        @prefix brick: <https://brickschema.org/schema/Brick#> .

        Result:
        @prefix bldg: <https://example.com/bldg#> .
        @prefix brick: <https://brickschema.org/schema/Brick#> .
        @prefix nsp: <https://w3id.org/se/building/nsp#> .
    """

    def extract_prefixes(lines):
        """Extracts @prefix declarations from TTL lines."""
        return {line.strip() for line in lines if line.strip().startswith("@prefix")}

    def filter_non_prefix_lines(lines):
        """Filters out @prefix declarations and blank lines."""
        return [line for line in lines if not line.strip().startswith("@prefix") and line.strip()]

    # Read and process the first file
    with open(f1, 'r') as f:
        data1 = f.readlines()
        prefixes1 = extract_prefixes(data1)
        non_prefix_data1 = filter_non_prefix_lines(data1)

    # Read and process the second file
    with open(f2, 'r') as f:
        data2 = f.readlines()
        prefixes2 = extract_prefixes(data2)
        non_prefix_data2 = filter_non_prefix_lines(data2)

    # Combine unique prefixes
    all_prefixes = sorted(prefixes1 | prefixes2)

    # Write to the output file
    with open(output_file, 'w') as f:
        # Write unique prefixes first
        f.writelines(line + "\n" for line in all_prefixes)
        f.write("\n")  # Add a blank line for separation
        # Write non-prefix content from both files
        f.writelines(non_prefix_data1)
        f.writelines(non_prefix_data2)

    print(f"Merged {f1} and {f2} into {output_file} successfully!")


# g1 = brickschema.Graph().load_file("bldg1")
# #validate(g1)

# g2 = brickschema.Graph().load_file("bldg2")
# #validate(g2)

# G = merge_type_cluster(g1, g2, BLDG, similarity_threshold=0.1)
# validate(G)
# G.serialize("merged.ttl", format="ttl")