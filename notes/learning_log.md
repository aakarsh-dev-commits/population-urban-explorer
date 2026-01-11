## Session 1 — Project Setup & Tooling Foundations

### Concepts Learned

- Python virtual environments isolate dependencies per project
- On macOS, `python3` is used to create venvs, not `python`
- The name of a virtual environment (e.g., `popenv`) is arbitrary
- Jupyter notebooks (`.ipynb`) are JSON files and must be created via Jupyter
- Jupyter creates `.ipynb_checkpoints` as auto-save backups
- Code quality tools serve different purposes:
  - Black → formatting
  - Ruff → linting and bug detection
  - Pytest → testing framework

### Why This Matters

A clean environment and repository structure prevent hidden bugs, reduce confusion, and make the project reproducible and professional.

### What I Did

- Created and activated a virtual environment
- Set up a clean project structure
- Installed and configured Black, Ruff, and Pytest
- Installed Jupyter inside the venv and created a valid notebook
- Cleaned up auto-generated files using `.gitignore`
- Fixed tooling warnings to keep the repo future-proof

## Session 2 — Loading World Boundaries & GeoDataFrames

### Concepts Learned

- A GeoDataFrame extends a Pandas DataFrame by adding a `geometry` column
- Shapefiles are multi-file datasets (`.shp`, `.dbf`, `.shx`, `.prj`) and must be kept together
- Natural Earth Admin-0 (countries) is cultural vector data suitable for population analysis
- CRS metadata is embedded in spatial data and must be checked explicitly
- EPSG:4326 (WGS84) is good for visualization but not for area calculations

### Why This Matters

Spatial analysis depends on both attribute data and geometry. Verifying CRS, geometry types, and dataset integrity early prevents incorrect calculations later (especially for area and density).

### What I Did

- Downloaded Natural Earth Admin-0 (110m) country boundaries
- Stored raw geospatial data on an external SSD
- Linked the dataset into the repo using a symbolic link
- Loaded the dataset into GeoPandas using a path variable
- Inspected columns, CRS, geometry types, and dataset shape
- Successfully plotted a global map of country boundaries

### Key Takeaways

Plotting is not just visualization — it is a validation step to confirm that spatial data is correctly loaded and interpreted.
