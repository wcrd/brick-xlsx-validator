import brick_xlsx_validator as bv
import os

df, bad_refs = bv.validate(os.path.join(r"C:\Users\WillDavidson\Desktop\DB-BrickModelInput-V6.xlsx"))