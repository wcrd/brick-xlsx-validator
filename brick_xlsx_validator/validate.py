import logging
import pandas as pd
from typing import Tuple
import rdflib

from .relationships import BRICK_RELATIONSHIPS
from . import validators as vd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate(
    filepath, 
    load_brick: bool = True, 
    load_switch: bool = True, 
    brick_version: str = "1.2", 
    switch_version: str = "1.1.7",
    path_to_local_brick: str = None, 
    path_to_local_switch: str = None,  
    custom_graph: rdflib.Graph = None, 
    reference_field: tuple = ("General","uuid")
) -> Tuple[pd.DataFrame, set, list]:
    """
    Validate checks that:
    1. Input excel has sheets for Equipment, Locations, and Points and that the bare minimum expected headers are provided.
    2. Validates that the provided reference column is valid (default: ("General", "uuid")).
    3. Validates that each entity is only defined once (is unique)
    4. Validates that all referenced entities exist
    5. Validates that classes used exist in Brick, Switch, or user provided ontology

    @params:
    custom_graph: A rdflib.Graph that can be used for validating classes against (i.e. in addition to Brick and Switch ontologies).
    reference_field: Tuple containing the column multi-header tuple for the input excel file field to be used as the 'reference' field; 
                    i.e. what field has been referenced by other entities in their relationship fields.
                    Defaults is the ('General', 'uuid') column, but it is common to use the ('Brick', 'label') column instead
    path_to_local_brick: Absolute path to local TTL to use as the Brick ontology. Only evaluated if load_brick=False
    path_to_local_switch: Absolute path to local TTL to use as the Switch ontology. Only evaluated if load_switch=False

    Returns:
    bad_rows: pandas dataframe containing the 'bad' rows from the read file, including the errors found for that row
    bad_refs: set of non-existing entities (i.e. bad references)
    bad_classes: set of invalid classes
    duplicates: list of pandas dataframes containing rows with duplicated ids per sheet 
    
    Most of this function should be replaced by pandas validation package
    """
    try:
        xlFile = pd.ExcelFile(filepath)

        # validate sheets
        dfs, errors = vd.readAndValidateExcelFile(xlFile)

        # validate important columns exist
        vd.validateIdentifierColumns(dfs)

        # validate reference_field exists
        vd.validateReferenceColumn(dfs, reference_field)

        # generate list of entities by reference_field
        entities_by_referenced_field = pd.concat([df[reference_field] for df in dfs.values()],
                             ignore_index=True)

        # generate list of model subjects
        # subjects = pd.concat([df['Brick']['identifier'] for df in dfs.values()],
        #                      ignore_index=True)

        # validate that subjects are unique
        all_unique, duplicate_ids = vd.validateUniqueness(dfs, ("Brick", "identifier"))

        # validate sheet references against this list
        bad_rows, bad_references = vd.validateReferences(dfs, entities_by_referenced_field, "Brick", BRICK_RELATIONSHIPS)

        # validate subjects are valid Brick or Switch entities
        classes = pd.concat([df['Brick']['class'] for df in dfs.values()], ignore_index=True).drop_duplicates().dropna()
        bad_classes = vd.validateClasses(classes, load_brick, load_switch, brick_version, switch_version, path_to_local_brick, path_to_local_switch, custom_graph)

        logger.info(f"Process complete.")
        logger.info(f" {len(bad_rows)} entities with bad references found in file {filepath} with a total of {len(bad_references)} instances of bad references")

        return bad_rows, set(bad_references), bad_classes, duplicate_ids

    except Exception as e:
        logger.error(f"Failed to process file {filepath} due to errors in the file")
        logger.error(e)



