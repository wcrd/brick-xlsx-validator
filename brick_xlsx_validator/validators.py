import pandas as pd
import logging
from typing import Tuple
import pkgutil
import rdflib
import io

from . import helpers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def readAndValidateExcelFile(xlFile: pd.ExcelFile) -> Tuple[dict, list]:
    sheets = ['equipment', 'locations', 'points']
    output = {}
    errors = []
    for sheet in sheets:
        try:
            output[sheet] = pd.read_excel(xlFile, sheet_name=sheet, header=[0, 1], dtype=str)
        except ValueError as e:
            logger.warning(f"Input file is missing sheet: {sheet}")
            errors.append(e)

    return output, errors


def validateIdentifierColumns(dfs:dict):
    for k, df in dfs.items():
        if helpers.validate_relationships(df['Brick'].columns, [("identifier", "Literal", "")]) == []:
            logger.warning(f"No valid identifier column found in {k} df. Aborting.")
            raise ValueError(f"No valid identifier column found in {k} df.")
        logger.info(f"--> SUCCESS. Validated identifiers for {k}")


def validateClasses(classes: pd.Series, load_brick: bool, load_switch: bool, brick_version: str, switch_version: str, custom_graph: rdflib.Graph = None):
    g = rdflib.Graph()
    bad_classes = []

    if load_brick:
        logger.info("Loading Brick Ontology for validation")
        # get ontology data from package
        data = pkgutil.get_data(
            __name__, f"ontologies/Brick/{brick_version}/Brick.ttl"
        ).decode()
        # wrap in StringIO to make it file-like
        g.parse(source=io.StringIO(data), format="turtle")

    if load_switch:
        logger.info("Loading Switch Ontology for validation")
        # get ontology data from package
        data = pkgutil.get_data(
            __name__, f"ontologies/Switch/{switch_version}/Brick-SwitchExtension.ttl"
        ).decode()
        # wrap in StringIO to make it file-like
        g.parse(source=io.StringIO(data), format="turtle")

    if custom_graph:
        logger.info("Loading custom ontology for validation")
        g = g + custom_graph

    ns = helpers.generate_namespaces(g)
    valid_classes = list(filter(lambda x: "#" in x.toPython(), g.subjects()))

    for cls in classes:
        if "switch:" in cls:
            cls = helpers.format_fragment(cls.replace("switch:", ""))
            namespace = "switch"
        else:
            cls = helpers.format_fragment(cls)
            namespace = "brick"

        if ns[namespace][cls] not in valid_classes:
            logger.warning(f"{namespace}:{cls} is not a valid {namespace} class")
            bad_classes.append(cls)

    logger.info(f"Completed checking classes. {len(bad_classes)} bad classes found.")
    return bad_classes


def validateReferences(dfs, subjects, ontologyName: str, relationships_to_process: list) -> Tuple[pd.DataFrame, list]:
    """
    For each relationship in relationships_to_process, check that all referenced entities exist in the subjects list
    :param dfs: dfs to validate
    :param subjects: list of valid subjects in the graph
    :param ontologyName: "Brick" or "Switch"
    :param relationships_to_process: Brick or Switch relationship tuples to validate
    :return:
    """
    logger.info(f"Processing {ontologyName} relationships.")
    bad_refs_list = []      # simple list of bad subject references
    bad_entries_list = []   # dataframe rows containing bad references

    for sheet, df in dfs.items():
        bad_refs_sheet = []

        # validate that ontology columns exist in the dataframe
        headerExists = ontologyName in df.columns
        if not headerExists:
            logger.warning(f"No {ontologyName} columns have been provided in sheet: {sheet}\nMoving to next sheet.")
            continue

        # get relationships defined in the model
        relationships = helpers.validate_relationships(df[ontologyName].columns, relationships_to_process)
        # filter relationships to just refs
        relationships = [rel for rel in relationships if rel.datatype == "ref"]
        logger.info(f"Sheet: {sheet} has the following relationships defined:")
        for rel in relationships: logger.info(f"\t {rel}")

        # process each relationship and check reference is valid
        for idx, row in df[ontologyName].iterrows():
            for rel in relationships:
                refs = row[rel.name]    # this may be multiple refs separated by "|"
                if not helpers.isReference(refs): continue

                refs = [ref.strip() for ref in refs.split("|")]
                bad_refs = [ref for ref in refs if ref not in subjects.values]
                if bad_refs:
                    # save bad subjects
                    bad_refs_sheet.extend(bad_refs)
                    # save entire row
                    data = dict(row)
                    data["Sheet"] = sheet
                    data["Bad References"] = bad_refs
                    bad_entries_list.append(data)

        bad_refs_list.extend(bad_refs_sheet)
        if bad_refs_sheet:
            logger.warning(f" {len(bad_refs_sheet)} bad references found for sheet: {sheet}")
        else:
            logger.info(f"--> SUCCESS. All references on sheet {sheet} are valid.")



    return pd.DataFrame(bad_entries_list), bad_refs_list