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