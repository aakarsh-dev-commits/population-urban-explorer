from src.io import load_countries, load_population
from src.preprocessing import reproject_equal_area, reproject_geographic, merge_population, compute_display_columns
from src.metrics import compute_area_km2, compute_population, compute_pop_density, compute_log_density
from src.visualization import plot_static_chloropleth, plot_interactive_choropleth, plot_globe, generate_high_end_globe_html

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

    # 4. Visualizations
    print("🎨 Generating visualizations...")
    
    import os
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

    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()
