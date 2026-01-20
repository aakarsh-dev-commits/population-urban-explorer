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

# Session 6 — Global Population Density Visualization (Log Scale)

## Objective

Visualize global population density in a way that preserves meaningful differences between countries with extremely uneven population distributions.

---

## Key Problems Identified

- Population density varies across **multiple orders of magnitude** (e.g., <1 to >1000 people/km²).
- Linear color scaling caused most countries to collapse into similar colors.
- EPSG:4326 (degrees) produces incorrect area calculations.

---

## Core Concepts Learned

### 1. Why Log Scaling is Necessary

- Linear scales hide variation when data is exponentially distributed.
- Log scaling spreads values across orders of magnitude.
- Enables meaningful visual comparison between low-density and high-density regions.

**Conclusion:** Log scale is more appropriate than linear or quantile for global population density.

---

### 2. Correct CRS for Area Computation

- EPSG:4326 → degrees → invalid for area
- EPSG:6933 → equal-area projection → meters

```python
world_eq = world.to_crs("EPSG:6933")
world_eq["area_km2"] = world_eq.geometry.area / 1e6
```

# Session 7 — Interactive Global Population Density Map (2D)

## Objective

Build a scientifically correct and interactive global population density map that:

- Preserves mathematical correctness of density values
- Uses log scaling to handle extreme variance
- Is visually interpretable and user-friendly

---

## Key Concepts Learned

### 1. Separation of CRS by Purpose

- **EPSG:6933 (equal-area)** was used for computing:
  - country area
  - population density
- **EPSG:4326 (WGS84)** was required for:
  - GeoJSON export
  - Plotly / web-based visualization

This reinforced the rule:

> _Compute in equal-area CRS, visualize in geographic CRS._

---

### 2. Why Log Scaling Is Necessary

Population density varies by several orders of magnitude globally.

Using a linear scale:

- Collapses most countries into the same color
- Makes meaningful comparison impossible

Using `log10(pop_density)`:

- Preserves relative ratios
- Makes both sparse and dense regions distinguishable
- Keeps the visualization scientifically defensible

---

### 3. Choropleth as a Data–Geometry Join

An interactive choropleth is fundamentally:

- A **tabular dataset**
- Joined to **geographic features**
- Using a shared identifier (`ADM0_A3` / ISO-3)

Plotly internally performs this join using:

- `locations` (DataFrame column)
- `featureidkey` (GeoJSON property)

---

### 4. GeoDataFrame → GeoJSON Conversion

Plotly does not accept GeoPandas objects directly.

Workflow:

1. Reproject geometry to EPSG:4326
2. Convert GeoDataFrame to GeoJSON via `.to_json()`
3. Load into Python dict with `json.loads()`

This step is essential for correct rendering.

---

### 5. Separation of Computation vs Presentation Columns

To keep tooltips readable:

- Raw computation columns were preserved
- Separate `_disp` columns were created for display
  - Rounded values
  - Human-friendly formatting

This follows clean data design principles.

---

### 6. Hover Semantics and UI Design

Hover tooltips were explicitly designed to show:

- Country name
- Area (km²)
- Population
- Population density (people/km²)

Internal or technical fields (ISO codes, log values) were hidden.

This improved interpretability without sacrificing rigor.

---

## Outcome

- Successfully built an interactive 2D global population density map
- Validated correct CRS handling
- Confirmed log-scaled density is the canonical metric for the project
- Established a reusable visualization pipeline for future projections

---

# Session 8 — 3D Interactive Globe (Population Density)

## Objective

Extend the interactive visualization layer by rendering global population density on a 3D globe, while preserving the exact same data, scaling, and methodology established in earlier sessions.

---

## Key Concepts Learned

### 1. Projection Changes Perception, Not Data

- The underlying dataset (population density) remained unchanged.
- Only the **map projection** changed from 2D to 3D (orthographic).
- This reinforced the idea that visualization alters _how_ data is perceived, not _what_ the data represents.

---

### 2. Orthographic Projection for Global Intuition

- The orthographic projection simulates viewing Earth from space.
- It preserves hemispheric relationships and spatial adjacency.
- Helps identify continental-scale patterns that can be visually distorted or flattened in 2D maps.

---

### 3. Reuse of a Stable Visualization Pipeline

The 3D globe reused:

- EPSG:4326 geometries
- `log_density` as the canonical metric
- ISO-3 / ADM0_A3 join logic
- Hover semantics (country name, area, population, density)

No recomputation or re-binning was introduced.

---

### 4. Consistency Across Visual Representations

- High-density regions (South Asia, parts of Europe) appeared consistently prominent.
- Low-density regions (Canada, Australia, Russia) remained subdued.
- Rotating the globe changed perspective but not meaning.

This validated that the visualization pipeline was robust.

---

### 5. Role of 3D Visualization in GIS

- 3D globes are best used for **exploration and intuition**, not measurement.
- Quantitative analysis must still rely on correct projections and numerical computation.
- The globe complements, rather than replaces, 2D analytical maps.

---

## Outcome

- Successfully built an interactive 3D globe for global population density.
- Confirmed methodological consistency between static, 2D interactive, and 3D views.
- Completed the visualization component of Phase 1.

---
