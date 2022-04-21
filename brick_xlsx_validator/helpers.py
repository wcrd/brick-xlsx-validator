import logging
import rdflib
from typing import Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Validate URIs
# TODO: Is there an official way to do this??
# RDF does not like whitespace or "/" in the URI fragment
def format_fragment(fragment):
    if isinstance(fragment, str):
        return fragment.replace(" ", "_").replace("/", "_")
    else:
        return fragment


def isReference(fragment):
    if isinstance(fragment, str): return True
    return False


# Validate relationships
# check pandas df has required relationships for brick model
def validate_relationships(df_headers, relationships_to_process):
    """
    Checks the pandas df has required relationships for brick model

    Params:
    df: pandas dataframe header (with relationships as column headers)
    relationships_to_process: list of tuples (relationship name, relationship datatype)
        * relationship datatype options: "", "Literal"
        * if the relationship datatype is "" then the type is assumed to be a reference to another object in the graph

    Returns: List of valid relationship tuples for given dataframe
    """
    relationships = []
    for relationship in relationships_to_process:
        if relationship[0] in df_headers:
            relationships.append(relationship)
        else:
            logger.debug(f"Input df does not have relationship: {relationship} defined.")

    return relationships

# Validate column exists
# Checks to see if multilevel column exists
def validate_column(df_headers, column_tuple) -> Tuple[bool, list]:
    '''
    Checks if the given multilevel column field exists in the given column set.

    Returns: column exists->bool
    '''
    return column_tuple in df_headers

def generate_namespaces(graph: rdflib.Graph) -> dict:
    # generate callable Namespace objects from Graph
    namespaceURIs = dict(graph.namespaces())
    # create namespace objects to make querying easier
    return {name: rdflib.Namespace(URI) for name, URI in namespaceURIs.items()}
