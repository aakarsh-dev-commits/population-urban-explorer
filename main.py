import os
import numpy as np
from src.io import load_countries, load_population
from src.preprocessing import reproject_equal_area, reproject_geographic, merge_population, compute_display_columns
from src.metrics import compute_area_km2, compute_population, compute_pop_density, compute_log_density
from src.analysis import compute_hotspots, compute_clusters, compute_idw_grid
from src.visualization import (
    plot_static_chloropleth, plot_interactive_choropleth, plot_globe, 
    generate_high_end_globe_html, plot_interactive_hotspots, plot_hotspots_globe, 
    plot_interactive_clusters, plot_clusters_globe, plot_idw_surface,
    plot_interactive_idw_surface, generate_hotspots_globe_html, generate_clusters_globe_html
)

def main():
    print("🚀 Starting Population Urban Explorer Pipeline...")

    # 1. Load Data
    print("📦 Loading data...")
    world = load_countries()
    
    # 2. Preprocessing & Merge
    print("⚙️  Preprocessing and merging data...")
    # Reproject to equal area for accurate area calculation
    world_eq = reproject_equal_area(world)
    
    # Calculate Area
    world_eq = compute_area_km2(world_eq)
    
    # Merge Population
    world_pop = merge_population(world_eq)
    
    # 3. Compute Metrics
    print("🧮 Computing metrics...")
    world_pop = compute_population(world_pop)
    world_pop = compute_pop_density(world_pop)
    world_pop = compute_log_density(world_pop)
    
    # Add display columns
    world_pop = compute_display_columns(world_pop)

    print("📊 Running advanced spatial analysis...")
    world_pop = compute_hotspots(world_pop)
    world_pop = compute_clusters(world_pop, n_clusters=5)

    # 4. Visualizations
    print("🎨 Generating visualizations...")
    os.makedirs("web/assets", exist_ok=True)

    # Static Plot
    print("   - Generating static map...")
    fig_static = plot_static_chloropleth(world_pop)
    fig_static.savefig("web/assets/static_population_density.png")
    print("     Saved to web/assets/static_population_density.png")

    # Interactive Plot
    print("   - Generating interactive map...")
    fig_interactive = plot_interactive_choropleth(world_pop)
    fig_interactive.write_html("web/assets/interactive_population_density.html")
    print("     Saved to web/assets/interactive_population_density.html")
    
    # Globe Plot (High-End)
    print("   - Generating High-End 3D globe...")
    generate_high_end_globe_html(world_pop, "web/assets/globe_population_density.html")
    print("     Saved to web/assets/globe_population_density.html")

    print("   - Generating Hotspots Interactive map & Globe...")
    fig_hotspot = plot_interactive_hotspots(world_pop)
    fig_hotspot.write_html("web/assets/interactive_hotspots.html")
    generate_hotspots_globe_html(world_pop, "web/assets/globe_hotspots.html")

    print("   - Generating Clusters Interactive map & Globe...")
    fig_cluster = plot_interactive_clusters(world_pop)
    fig_cluster.write_html("web/assets/interactive_clusters.html")
    generate_clusters_globe_html(world_pop, "web/assets/globe_clusters.html")

    print("   - Generating IDW Surface...")
    valid = world_pop.dropna(subset=['log_density']).copy()
    valid_plot = valid.to_crs("EPSG:4326")
    # For accurate spatial queries, it's actually better to use equal-area centroids for the tree search, 
    # but the grid needs to align with the visual extent (EPSG 4326 bounds)
    # Using geographic centroids directly for distance isn't physically accurate but acceptable for web viz.
    # To avoid scipy cKDTree spherical distance issues, we use nearest neighbor weighting.
    with np.errstate(invalid='ignore'):
        points = np.c_[valid_plot.geometry.centroid.x, valid_plot.geometry.centroid.y]
        values = valid_plot['log_density'].values
        minx, miny, maxx, maxy = valid_plot.total_bounds
        grid_x, grid_y = np.mgrid[minx:maxx:300j, miny:maxy:150j]
        grid_z = compute_idw_grid(points, values, grid_x, grid_y)
    
    fig_idw = plot_idw_surface(grid_x, grid_y, grid_z, world_pop)
    fig_idw.savefig("web/assets/static_idw_surface.png")
    
    print("   - Generating Interactive IDW Surface...")
    from src.visualization import plot_interactive_idw_surface
    fig_interactive_idw = plot_interactive_idw_surface(world_pop)
    fig_interactive_idw.write_html("web/assets/interactive_idw_surface.html")
    print("     Saved interactive IDW surface HTML")

    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()
