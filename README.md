# brick-xlsx-validator

A tool that performs basic structure validation on brick models constructed in excel using the provided template [link to template].

## Validations

The tool validates the following:
* Main definition sheets exist: Equipment, Locations, Points
* Entities have an ID defined
* Entities have a valid class defined (either from Brick, or provided custom ontology)
* Relationships per entity reference other defined entities

## Example Usage

```python
import brick_xlsx_validator as bv
import os

model_path = r"path_to_excel/excel_file.xlsx"

df, bad_refs, bad_classes = bv.validate(os.path.join(model_path))
```

The validator can take a number of options:
```python
validate(filepath, load_brick: bool = True, load_switch: bool = True, brick_version: str = "1.2", switch_version: str = "1.1", custom_graph: rdflib.Graph = None)
```
`custom_graph`: a custom ontology definition in .ttl format that can be used for class validation

The output of the validator is:
* pandas dataframe containing the 'bad' rows from the read file, including the errors found for that row
* set of non-existing entities (i.e. bad references)
* set of invalid classes

## Installation
Create a new environment and install from github:

 ```
 poetry add git+https://github.com/wcrd/brick-xlsx-validator.git@main
 ```
 In your working file simply import the package

 ```python
 import brick_xlsx_validator as bv
 ```
An example working file is provide as 'example.py'.