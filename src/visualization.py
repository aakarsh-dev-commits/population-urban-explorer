import numpy as np
import matplotlib.pyplot as plt
import json
import geopandas as gpd
import plotly.express as px
import plotly.io as pio


def plot_static_chloropleth(world_pop):
    log_ticks = np.array([-1,0,1,2,3])

    fig , ax = plt.subplots(1,1, figsize=(15,18))

    world_pop.plot(
        column = "log_density",
        cmap = "viridis",
        linewidth=0.2,
        ax = ax,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        },
        legend=True
    )

    cbar = ax.get_figure().axes[-1]

    cbar.yaxis.set_ticks(log_ticks)
    cbar.yaxis.set_ticklabels([f"{np.power(10.0, t):g}" for t in log_ticks])


    ax.set_title(
        "Global Population Density (log-scaled, people per km2)",
        fontsize=14
    )

    ax.axis("off")
    
    return fig


def plot_interactive_choropleth(world_pop):
    world_plot = world_pop.to_crs("EPSG:4326")
    geojson = json.loads(world_plot.to_json())

    fig = px.choropleth(
        world_plot,
        geojson=geojson,
        locations="ADM0_A3",
        featureidkey="properties.ADM0_A3",
        color="log_density",
        color_continuous_scale="viridis",
        hover_name="ADMIN",
        hover_data={
            "area_km2_disp": True,
            "population_disp": True,
            "pop_density_disp": True,
            "log_density": False,
            "ADM0_A3": False
        },
        labels={
            "area_km2_disp": "Area (km²)",
            "population_disp": "Population",
            "pop_density_disp": "Population density (people/km²)"
        }
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        projection_type="natural earth"
    )

    fig.update_layout(
        title="Global Population Density (people per km², log-scaled)",
        coloraxis_colorbar=dict(
            title="Population density<br>(log scale)"
        ),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    return fig


def plot_globe(world_pop):
    world_plot = world_pop.to_crs("EPSG:4326")
    geojson = json.loads(world_plot.to_json())

    fig = px.choropleth(
        world_plot,
        geojson=geojson,
        locations="ADM0_A3",
        featureidkey="properties.ADM0_A3",
        color="log_density",
        color_continuous_scale="viridis",
        hover_name="ADMIN",
        hover_data={
            "area_km2_disp": True,
            "population_disp": True,
            "pop_density_disp": True,
            "log_density": False,
            "ADM0_A3": False
        },
        labels={
            "area_km2_disp": "Area (km²)",
            "population_disp": "Population",
            "pop_density_disp": "Population density (people/km²)"
        }
    )

    # 🔑 Switch to globe
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=False,
        showcountries=False,
        showframe=False
    )

    fig.update_layout(
        title="Global Population Density (3D Globe, log-scaled)",
        coloraxis_colorbar=dict(
            title="Population density<br>(log scale)"
        ),
        margin={"r":0, "t":40, "l":0, "b":0}
    )
    
    return fig



def generate_high_end_globe_html(world_pop, output_path):
    """
    Generates a high-end 3D globe HTML file using Globe.gl.
    Uses 'Laser Beams' (Points) to represent population density from country centroids.
    """
    # Prepare Data
    # 1. Background Polygons (Wireframes) - Keep in lat/lon
    world_plot = world_pop.to_crs("EPSG:4326")
    geojson_str = world_plot.to_json()
    
    # 2. Centroid Lasers - PROJECT FIRST for accurate centroids
    # Reproject to equal area (EPSG:8857 or similar) for centroid calc
    world_projected = world_pop.to_crs("EPSG:6933") 
    centroids_projected = world_projected.geometry.centroid
    
    # Reproject centroids back to Lat/Lon (EPSG:4326)
    centroids = centroids_projected.to_crs("EPSG:4326")
    
    points_data = []
    # Iterate using the original world_plot to keep metadata, but use calculated centroids
    for idx, row in world_plot.iterrows():
        val = row['log_density']
        if np.isfinite(val):
             # Match by index
             cent = centroids.loc[idx]
             points_data.append({
                'lat': cent.y,
                'lng': cent.x,
                'val': val,
                'country': row['ADMIN'],
                'pop': row['population_disp'],
                'density': row['pop_density_disp']
             })
            
    points_json = json.dumps(points_data)
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #000; }}
        #globeViz {{ width: 100vw; height: 100vh; }}
    </style>
    <script src="//unpkg.com/globe.gl"></script>
</head>
<body>
<div id="globeViz"></div>

<script>
    // Data
    const polygonData = {geojson_str};
    const pointData = {points_json};
    
    console.log('Point data loaded:', pointData.length, 'countries');
    
    // Custom color function - bright yellow to red gradient
    function getColor(t) {{
        // t is 0 to 1
        // Go from yellow (low) to orange to red (high)
        const r = 255;
        const g = Math.round(255 * (1 - t * 0.7));
        const b = Math.round(50 * (1 - t));
        return `rgb(${{r}},${{g}},${{b}})`;
    }}
    
    // Initialize globe after short delay to ensure DOM is ready
    setTimeout(function() {{
        console.log('Initializing globe...');
        
        // Normalize: log_density ~ -1 to 5
        const normalize = v => Math.max(0, Math.min(1, (v + 1) / 6));
        
        const myGlobe = Globe()
            .globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
            .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
            
            // Country Borders
            .polygonsData(polygonData.features)
            .polygonCapColor(() => 'rgba(0,0,0,0)')
            .polygonSideColor(() => 'rgba(0,0,0,0)')
            .polygonStrokeColor(() => 'rgba(0, 255, 255, 0.3)')
            .polygonAltitude(0.006)
            
            // LASER BEAMS - All 167 points!
            .pointsData(pointData)
            .pointLat(d => d.lat)
            .pointLng(d => d.lng)
            .pointAltitude(d => Math.max(0.1, normalize(d.val) * 0.8))
            .pointRadius(0.5)
            .pointColor(d => getColor(normalize(d.val)))
            .pointResolution(12)
            .pointsMerge(false)
            
            // Tooltip
            .pointLabel(d => `<div style="background:rgba(0,0,0,0.8);color:#fff;padding:10px;border-radius:5px;"><b>${{d.country}}</b><br/>Pop: ${{Math.round(d.pop).toLocaleString()}}<br/>Density: ${{d.density}}/km²</div>`)
            
            (document.getElementById('globeViz'));
        
        // Controls
        myGlobe.controls().autoRotate = true;
        myGlobe.controls().autoRotateSpeed = 0.5;
        myGlobe.pointOfView({{ altitude: 2.5 }});
        
        console.log('Globe initialized with', myGlobe.pointsData().length, 'points');
    }}, 100);
</script>

</body>
</html>
'''


    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return output_path

HOTSPOT_COLORS = {
    "High-High (Hotspot)": "red",
    "Low-Low (Coldspot)": "blue",
    "High-Low": "lightblue",
    "Low-High": "orange",
    "Not Significant": "lightgrey",
    "No Data": "white"
}

def plot_interactive_hotspots(world_pop):
    world_plot = world_pop.to_crs("EPSG:4326")
    geojson = json.loads(world_plot.to_json())

    fig = px.choropleth(
        world_plot,
        geojson=geojson,
        locations="ADM0_A3",
        featureidkey="properties.ADM0_A3",
        color="hotspot_category",
        color_discrete_map=HOTSPOT_COLORS,
        hover_name="ADMIN",
        hover_data={
            "hotspot_category": True,
            "pop_density_disp": True,
            "ADM0_A3": False
        },
        labels={"hotspot_category": "Hotspot Category", "pop_density_disp": "Pop Density"}
    )
    fig.update_geos(showframe=False, showcoastlines=False, projection_type="natural earth")
    fig.update_layout(title="Population Density Hotspots (Local Moran's I)", margin={"r":0,"t":40,"l":0,"b":0})
    return fig


def plot_hotspots_globe(world_pop):
    fig = plot_interactive_hotspots(world_pop)
    fig.update_geos(projection_type="orthographic", showcoastlines=False, showcountries=False, showframe=False)
    fig.update_layout(title="Population Density Hotspots (3D Globe)")
    return fig


def plot_interactive_clusters(world_pop):
    world_plot = world_pop.to_crs("EPSG:4326")
    geojson = json.loads(world_plot.to_json())

    fig = px.choropleth(
        world_plot,
        geojson=geojson,
        locations="ADM0_A3",
        featureidkey="properties.ADM0_A3",
        color="cluster",
        color_discrete_sequence=px.colors.qualitative.Set1,
        hover_name="ADMIN",
        hover_data={
            "cluster": True,
            "pop_density_disp": True,
            "ADM0_A3": False
        },
        labels={"cluster": "KMeans Cluster"}
    )
    fig.update_geos(showframe=False, showcoastlines=False, projection_type="natural earth")
    fig.update_layout(title="Population & Density Clusters", margin={"r":0,"t":40,"l":0,"b":0})
    return fig


def plot_clusters_globe(world_pop):
    fig = plot_interactive_clusters(world_pop)
    fig.update_geos(projection_type="orthographic", showcoastlines=False, showcountries=False, showframe=False)
    fig.update_layout(title="Population & Density Clusters (3D Globe)")
    return fig

def plot_idw_surface(grid_x, grid_y, grid_z, world_pop):
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    
    contour = ax.contourf(grid_x, grid_y, grid_z, levels=50, cmap="viridis", alpha=0.9)
    
    world_plot = world_pop.to_crs("EPSG:4326")
    world_plot.boundary.plot(ax=ax, linewidth=0.4, color="white", alpha=0.6)
    
    cbar = fig.colorbar(contour, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("Log Population Density")
    
    ax.set_title("IDW Interpolated Population Density Surface", fontsize=14)
    ax.set_aspect('auto')
    ax.axis("off")
    
    return fig


def plot_interactive_idw_surface(world_pop):
    valid = world_pop.dropna(subset=['log_density']).copy()
    valid_plot = valid.to_crs("EPSG:4326")
    
    valid_plot['centroid_lat'] = valid_plot.geometry.centroid.y
    valid_plot['centroid_lon'] = valid_plot.geometry.centroid.x
    
    fig = px.density_mapbox(
        valid_plot, 
        lat='centroid_lat', 
        lon='centroid_lon', 
        z='log_density',
        radius=40,
        center=dict(lat=20, lon=0), 
        zoom=0.8,
        mapbox_style="carto-darkmatter",
        color_continuous_scale="viridis",
        hover_name="ADMIN"
    )
    
    fig.update_layout(
        title="Interactive Density Interpolation Surface", 
        margin={"r":0,"t":40,"l":0,"b":0},
        coloraxis_colorbar=dict(title="Log Density")
    )
    return fig
