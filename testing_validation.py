import os
import pandas as pd
from pandas import ExcelFile

from brick_xlsx_validator import helpers
from collections import namedtuple

# Define relationships of interest for this model
Rel = namedtuple("Rel", ['name', 'datatype', 'namespace'])

# Brick Relationships of interest (relationships, datatype (if not reference), namespace (if not brick))
BRICK_RELATIONSHIPS = [
    Rel("label", "Literal", "rdfs"),
    Rel("hasUuid", "Literal", "brick"),
    Rel("feeds", "ref", "brick"),
    Rel("isFedBy", "ref", "brick"),
    Rel("hasPart", "ref", "brick"),
    Rel("isPartOf", "ref", "brick"),
    Rel("hasLocation", "ref", "brick"),
    Rel("isLocationOf", "ref", "brick"),
    Rel("hasInputSubstance", "brick", "brick"),
    Rel("hasOutputSubstance", "brick", "brick"),
    Rel("hasUnit", "Literal", "brick"),
    Rel("isPointOf", "ref", "brick")
]

path_to_xlsx = os.path.join(r"C:\Users\WillDavidson\Desktop\DB\equipment2.xlsx")

xlFile = pd.ExcelFile(path_to_xlsx)
df_locations = pd.read_excel(xlFile, sheet_name="locations", header=[0, 1], dtype=str)
df_equipment = pd.read_excel(xlFile, sheet_name="equipment", header=[0, 1], dtype=str)
df_points = pd.read_excel(xlFile, sheet_name="points", header=[0, 1], dtype=str)

# generate entity list
# validate input df has a valid identifier column (this is used for entity definition).
# Df must have this column
if helpers.validate_relationships(df_locations['Brick'].columns, [("identifier", "Literal", "")]) == []:
    print("No valid identifier column found in locations df. Aborting.")
if helpers.validate_relationships(df_equipment['Brick'].columns, [("identifier", "Literal", "")]) == []:
    print("No valid identifier column found in equipment df. Aborting.")

entities = pd.concat([df_locations['Brick'][['identifier']], df_equipment['Brick'][['identifier']]], ignore_index=True)

def validate_refs(df, entities, multiIndexHeader: str, relationships_to_process: list):
    print(f"Processing {multiIndexHeader} relationships.")
    bad_refs_list = []
    bad_entries_list = []

    # validate that multi-index header has been provided
    # validate if input file has SwitchTags
    headerExists = multiIndexHeader in df.columns

    if not headerExists:
        print(f"No {multiIndexHeader} columns have been provided in both files")
        return triples

    # validate input df has a valid identifier column (this is used for entity definition).
    # Df must have this column
    if helpers.validate_relationships(df['Brick'].columns, [("identifier", "Literal", "")]) == []:
        print("No valid identifier column found in source df. Aborting.")
        return triples

    # validate input df has all relationships, return relationships that exist
    relationships = helpers.validate_relationships(df[multiIndexHeader].columns, relationships_to_process)
    # filter relationships to just refs
    relationships = [rel for rel in relationships if rel.datatype == "ref"]

    for idx, row in df[multiIndexHeader].iterrows():
        for rel in relationships:
            refs = row[rel.name]
            if not helpers.isReference(refs): continue
            refs = [ref.strip() for ref in refs.split("|")]
            badRefs = [ref for ref in refs if ref not in entities['identifier'].values]
            bad_refs_list.extend(badRefs)
            if badRefs:
                data = dict(row)
                data["Bad References"] = badRefs
                bad_entries_list.append(data)

    return pd.DataFrame(bad_entries_list), set(bad_refs_list)

brs, br_list = validate_refs(df_equipment, entities, "Brick", BRICK_RELATIONSHIPS)