import pandas as pd
import numpy as np
import geopandas as gpd

def compute_area_km2(world_eq: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  world_eq["area_km2"] = world_eq.geometry.area / 1e6
  return world_eq

def compute_population(world_pop: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  world_pop["population"] = pd.to_numeric(
    world_pop["2022 [YR2022]"],
    errors = "coerce"
    )
  return world_pop
  
def compute_pop_density(world_pop: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  world_pop["pop_density"] = (
    world_pop["population"] / world_pop["area_km2"]
    )
  return world_pop
  
def compute_log_density(world_pop: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  world_pop["log_density"] = np.log10(world_pop["pop_density"])
  return world_pop