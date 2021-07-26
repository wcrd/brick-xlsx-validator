import logging
import pandas as pd
from typing import Tuple

from .relationships import BRICK_RELATIONSHIPS
from . import validators as vd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate(filepath) -> Tuple[pd.DataFrame, set]:
    """Most of this function should be replaced by pandas validation package"""
    try:
        xlFile = pd.ExcelFile(filepath)

        # validate sheets
        dfs, errors = vd.readAndValidateExcelFile(xlFile)

        # validate important columns exist
        vd.validateIdentifierColumns(dfs)

        # generate list of model subjects
        subjects = pd.concat([df['Brick']['identifier'] for df in dfs.values()],
                             ignore_index=True)

        # validate sheet references against this list
        bad_rows, bad_references = vd.validateReferences(dfs, subjects, "Brick", BRICK_RELATIONSHIPS)

        logger.info(f"Process complete.")
        logger.info(f" {len(bad_rows)} entities with bad references found in file {filepath} with a total of {len(bad_references)} instances of bad references")

        return bad_rows, set(bad_references)

    except Exception as e:
        logger.error(f"Failed to process file {filepath} due to errors in the file")
        logger.error(e)



