from pathlib import Path

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_EQUAL_AREA = "EPSG:6933"
POP_YEAR_COL = "2022 [YR2022]"
JOIN_KEY = "ADM0_A3"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

COUNTRIES_DIR = PROJECT_ROOT/"data"/"raw"/"ne_countries"
POP_DIR = PROJECT_ROOT/"data"/"raw"/"population"/"world_bank"/"P_Data_Extract_From_World_Development_Indicators"

COUNTRIES_DATA2 = COUNTRIES_DIR / "ne_110m_admin_0_countries2"
POP_DATA = POP_DIR / "e90b26f6-5d7d-4ac6-ba24-89282b654ce4_Data.csv"