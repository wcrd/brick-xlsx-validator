import brick_xlsx_validator as bv
import os

# model_path = r"C:\Users\WillDavidson\Desktop\DB-BrickModelInput-V6.xlsx"
# model_path = r"C:\Users\WillDavidson\OneDrive - Switch Automation\R&D\Brick Modelling\sites\Carrier CIB\20210728 - Carrier-CiB_subParted _newFormat.xlsx"
# model_path = r"C:\Users\WillDavidson\OneDrive - Switch Automation\R&D\Brick Modelling\sites\Carrier CIB\20210728 - Carrier-CiB _newFormat.xlsx"
# model_path = r"C:\Users\WillDavidson\Downloads\eau_clair_equip.xlsx"
model_path = r"C:\Users\WillDavidson\OneDrive - Switch Automation\R&D\Brick Modelling\sites\Carrier Lerner\20210808 - Carrier-Lerner _newFormat.xlsx"

df, bad_refs, bad_classes = bv.validate(os.path.join(model_path), reference_field=("Brick", "label"))

