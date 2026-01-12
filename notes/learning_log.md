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

---

## Session 3 — CRS, Reprojection, and Area Computation

### Objective

Understand why coordinate reference systems (CRS) matter for numerical correctness and learn how to correctly compute geographic area for global datasets.

### Concepts Learned

- EPSG:4326 (WGS84) stores coordinates in angular units (degrees), not linear units
- Area calculations in a geographic CRS are mathematically invalid and misleading
- GeoPandas may allow incorrect computations to run, making CRS errors dangerous
- Projected CRSs use linear units (meters), enabling meaningful distance and area calculations
- Equal-area projections preserve surface area relationships across regions
- EPSG:6933 (World Cylindrical Equal Area) is suitable for global area comparisons

### What I Did

- Intentionally computed area in EPSG:4326 to observe warnings and incorrect results
- Interpreted GeoPandas warnings instead of ignoring them
- Reprojected the dataset to an equal-area CRS (EPSG:6933)
- Computed country areas in square meters and converted them to square kilometers
- Verified results using known country sizes and rankings
- Investigated unexpected outputs (Antarctica, USA vs China) and identified data semantics issues rather than computational bugs

### Key Technical Insights

- geometry.area returns values in the square of the CRS’s linear unit
- Dividing by 1e6 converts square meters to square kilometers
- Correct computation does not guarantee meaningful interpretation
- Domain context (e.g., sovereign countries vs territories) must be handled explicitly
- Data warnings are signals of conceptual problems, not noise

### Engineering Takeaways

- Never compute area or distance in EPSG:4326
- Always verify CRS before performing geometric calculations
- Store derived metrics (like area) once after correct computation
- Question outputs that contradict real-world intuition

### Outcome

A correctly reprojected global dataset with validated country areas in km², ready for population density calculations.
