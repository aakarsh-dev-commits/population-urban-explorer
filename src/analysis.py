import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial import cKDTree

import libpysal
import esda

def compute_hotspots(world_pop: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Ensure no missing values in target column
    df = world_pop.copy()
    
    # We need a metric for hotspots, e.g., 'log_density'
    valid_idx = df['log_density'].notna()
    
    # Work on a valid subset to compute weights and Local Moran's I
    valid_df = df[valid_idx].copy()
    
    # Needs projected geometry to calculate centroids and nearest neighbors. 
    # Use spatial weights (KNN=5) based on polygon centroids
    w = libpysal.weights.KNN.from_dataframe(valid_df, k=5)
    w.transform = 'r'
    
    y = valid_df['log_density'].values
    
    # Calculate Local Moran's I
    lisa = esda.moran.Moran_Local(y, w)
    
    # Categorize into Hotspots, Coldspots, etc.
    # Significant categories (p < 0.05)
    sig = lisa.p_sim < 0.05
    hotspots = sig * lisa.q
    
    # 1=HH, 2=LH, 3=LL, 4=HL
    # Map to strings
    labels = {0: "Not Significant", 1: "High-High (Hotspot)", 2: "Low-High", 3: "Low-Low (Coldspot)", 4: "High-Low"}
    
    hotspot_labels = [labels[val] for val in hotspots]
    valid_df['hotspot_category'] = hotspot_labels
    
    # Merge back
    df = df.join(valid_df[['hotspot_category']])
    df['hotspot_category'] = df['hotspot_category'].fillna("No Data")
    
    return df

def compute_clusters(world_pop: gpd.GeoDataFrame, n_clusters: int = 5) -> gpd.GeoDataFrame:
    df = world_pop.copy()
    
    # Features to cluster strictly with valid data
    features = ['log_density', 'area_km2', 'population']
    
    valid_idx = df[features].notna().all(axis=1)
    valid_df = df[valid_idx].copy()
    
    X = valid_df[features].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Convert cluster labels to string categories for plotting easily
    valid_df['cluster'] = [f"Cluster {c+1}" for c in clusters]
    
    df = df.join(valid_df[['cluster']])
    df['cluster'] = df['cluster'].fillna("No Data")
    return df

def compute_idw_grid(points, values, grid_x, grid_y, p=2.0, k=8):
    """
    points: (N, 2) arrays of projected x,y coordinates
    values: (N,) array of values
    grid_x, grid_y: 2D arrays forming a dense grid
    """
    grid_points = np.c_[grid_x.ravel(), grid_y.ravel()]
    tree = cKDTree(points)
    
    # Find k nearest neighbors to each grid point
    dists, idxs = tree.query(grid_points, k=k)
    
    # Avoid div-by-zero for exact matches
    dists = np.maximum(dists, 1e-10)
    
    weights = 1.0 / (dists ** p)
    
    z_interp = np.sum(weights * values[idxs], axis=1) / np.sum(weights, axis=1)
    
    return z_interp.reshape(grid_x.shape)
