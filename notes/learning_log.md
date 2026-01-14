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

## Session 4 — Population Data Ingestion & Join Resolution

### Objective

Attach reliable country-level population data to global country geometries while avoiding silent data corruption due to identifier mismatches.

---

### Work Done

- Downloaded World Bank **World Development Indicators** population data (`SP.POP.TOTL`) for **2022**
- Loaded Natural Earth Admin-0 country geometries
- Attempted initial population–geometry join
- Diagnosed unexpected missing population values after merge
- Investigated Natural Earth schema and identifier design
- Compared:
  - Admin-0 Countries vs Admin-0 Sovereignty datasets
  - Natural Earth versions **5.1.1 vs 5.0**
- Identified sovereignty vs ISO-3 mismatch (`SOV_A3 ≠ ISO-3`)
- Switched to **Admin-0 sovereignty v5.0** to obtain `ADM0_A3`
- Re-merged population data using ISO-3 (`ADM0_A3 ↔ Country Code`)
- Audited and documented remaining missing entities

---

### Key Learnings

#### 1. Country Names Are Unsafe Join Keys

- Human-readable names vary across datasets
- Minor political or spelling differences cause silent join failures
- ISO-3 codes are required for reliable cross-dataset joins

#### 2. Natural Earth Uses Multiple Identifier Semantics

- `SOV_A3` represents political sovereignty, not strict ISO-3
- Values like `US1`, `FR1`, `AU1` encode sovereignty groupings
- World Bank data uses **strict ISO-3**
- Identifier semantics must be understood before joining

#### 3. Dataset Versioning Affects Schema

- Natural Earth v5.1 prioritizes sovereignty representation
- Natural Earth v5.0 Admin-0 sovereignty exposes `ADM0_A3`
- Choosing the correct dataset version is a data-engineering decision

#### 4. Left Joins Are Essential for Validation

- Left joins expose mismatches and missing entities
- Inner joins would silently drop problematic records
- Explicit inspection of `NaN` rows is required for correctness

#### 5. Missing Data Can Be Correct

Remaining missing entities (e.g. Antarctica, Western Sahara, Somaliland, Northern Cyprus, Taiwan, Kosovo) are:

- Non-sovereign
- Politically indeterminate
- Or inconsistently reported by the World Bank

These exclusions are expected and defensible.

---

### Final Outcome

- Successfully merged global population data with country geometries using ISO-3
- No major sovereign countries missing
- All exclusions are explicit, documented, and explainable
- Phase 1 data foundation is now correct and trustworthy

---

### Concepts Locked In

- ISO-3 vs sovereignty identifiers
- Data integration vs cartographic representation
- Inspect before joining
- Validate before filtering
- Correctness over convenience

## Session 5 — Population Density Computation

### Objective

Compute physically meaningful population density values by combining correct population data with accurate country areas.

---

### Work Done

- Reprojected global country geometries from EPSG:4326 to **EPSG:6933** (equal-area)
- Computed country areas in square kilometers using projected geometry
- Diagnosed and resolved type errors in population data
- Converted World Bank population values from strings to numeric using safe coercion
- Calculated population density as people per km²
- Performed global sanity checks on area and density rankings

---

### Key Learnings

#### 1. EPSG:4326 Is Invalid for Area Calculations

- EPSG:4326 uses angular units (degrees), not linear units
- Polygon areas computed in degrees² have no physical meaning
- Area distortion varies with latitude
- Equal-area projections are mandatory for density calculations

#### 2. Equal-Area CRS Enables Correct Area Math

- EPSG:6933 preserves area globally
- Geometry area is computed in square meters
- Explicit conversion to km² ensures interpretable units

#### 3. CSV Numeric Columns Cannot Be Trusted

- World Bank population values were loaded as strings (`object` dtype)
- Arithmetic failed due to string–float operations
- Used `pd.to_numeric(errors="coerce")` to safely convert values
- Invalid entries were correctly converted to `NaN` instead of crashing

#### 4. Density Must Be Computed on a Consistent Dataset

- Population and area must exist in the same GeoDataFrame
- Mixing columns across DataFrames is fragile and unsafe
- Final density computation was performed on the merged, equal-area dataset

#### 5. Sanity Checks Are Mandatory

- Largest areas matched real-world expectations (Russia, Canada, USA, China)
- Highest population densities were observed in known dense countries (Bangladesh, Rwanda, India, Netherlands)
- Low-density regions behaved as expected
- Results were numerically and geographically plausible

---

### Final Outcome

- Successfully computed global population density (people per km²)
- All calculations are physically meaningful and defensible
- Dataset is now ready for visualization and spatial analysis

---

### Concepts Locked In

- Geographic CRS vs projected CRS
- Equal-area projections for density calculations
- Safe numeric coercion in pandas
- Importance of unit awareness
- Data validation through sanity checks
