from collections import namedtuple

# Define relationships of interest for this model
Rel = namedtuple("Rel", ['name', 'datatype', 'namespace'])

# Brick Relationships of interest (relationships, datatype (if not reference), namespace (if not brick))
BRICK_RELATIONSHIPS = [
    Rel("label", "Literal", "rdfs"),
    Rel("feeds", "ref", "brick"),
    Rel("isFedBy", "ref", "brick"),
    Rel("hasPart", "ref", "brick"),
    Rel("isPartOf", "ref", "brick"),
    Rel("hasLocation", "ref", "brick"),
    Rel("isLocationOf", "ref", "brick"),
    Rel("hasInputSubstance", "brick", "brick"),
    Rel("hasOutputSubstance", "brick", "brick"),
    Rel("hasUnit", "Literal", "brick"),
    Rel("isPointOf", "ref", "brick"),
    Rel("hasPoint", "ref", "brick"),
    Rel("meters", "ref", "brick"),          # V1.3
    Rel("isMeteredBy", "ref", "brick"),     # V1.3
    Rel("hasSubmeter", "ref", "brick"),     # V1.3
    Rel("isSubmeterOf", "ref", "brick")     # V1.3
]