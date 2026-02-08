import geopandas as gpd
from .config import CRS_EQUAL_AREA,CRS_GEOGRAPHIC,JOIN_KEY
from .io import load_countries, load_population

def reproject_equal_area(world: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  return world.to_crs(CRS_EQUAL_AREA)

def reproject_geographic(world: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  return world.to_crs(CRS_GEOGRAPHIC)

def merge_population(world: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  pop = load_population()
  world = world.merge(
    pop,
    how = "left",
    left_on = JOIN_KEY,
    right_on = "Country Code"
  )
  return world


def compute_display_columns(world_pop: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
  world_pop["area_km2_disp"] = world_pop["area_km2"].round(0)
  world_pop["population_disp"] = world_pop["population"].round(0)
  world_pop["pop_density_disp"] = world_pop["pop_density"].round(1)
  return world_pop