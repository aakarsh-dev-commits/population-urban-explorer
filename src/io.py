from pathlib import Path
import pandas as pd
import geopandas as gpd
from .config import COUNTRIES_DATA2, POP_DATA

def load_countries():
  return gpd.read_file(COUNTRIES_DATA2)

def load_population():
  return pd.read_csv(POP_DATA)

