import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap
import glob

# Input and output directories
input_dir = "data/raw/BlackMarbleMonthly21-26feb"
output_dir = "data/processed/images(streamlit)"

os.makedirs(output_dir, exist_ok=True)

# Custom colormap for night lights (black to yellow to white)
colors = ['#000000', '#0a0a2a', '#1a1a4a', '#2a2a6a', '#4a2a8a', 
          '#8a2a6a', '#ca2a4a', '#ff4a2a', '#ffaa2a', '#ffffaa', '#ffffff']
cmap = LinearSegmentedColormap.from_list('night_lights', colors, N=256)

# Get all HDF5 files
files = sorted(glob.glob(os.path.join(input_dir, "hk_lights_*.h5")))

print(f"Found {len(files)} files")

# Pre-calculate HK indices once
hk_lat_idx = None
hk_lon_idx = None

for file_path in files:
    # Extract year and month from filename
    basename = os.path.basename(file_path)
    parts = basename.split('_')
    if len(parts) >= 4:
        year = parts[2]
        month = parts[3]
    else:
        continue
    
    print(f"Processing {year}-{month}")
    
    with h5py.File(file_path, 'r') as f:
        lat = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lat'][:]
        lon = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lon'][:]
        
        # Get HK indices on first file
        if hk_lat_idx is None:
            lat_min, lat_max = 22.0, 22.6
            lon_min, lon_max = 113.7, 114.4
            hk_lat_idx = np.where((lat >= lat_min) & (lat <= lat_max))[0]
            hk_lon_idx = np.where((lon >= lon_min) & (lon <= lon_max))[0]
            
            # Get the actual lat/lon values for HK region
            hk_lat = lat[hk_lat_idx]
            hk_lon = lon[hk_lon_idx]
            
            print(f"HK region: {len(hk_lat_idx)} x {len(hk_lon_idx)} pixels")
        
        # Get radiance data
        radiance = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free'][:]
        hk_radiance = radiance[np.ix_(hk_lat_idx, hk_lon_idx)]
        
        # Filter out invalid values (negative or extreme)
        hk_radiance_clean = np.where((hk_radiance < 0) | (hk_radiance > 1000), 0, hk_radiance)
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(10, 12))
        
        # Plot the night lights
        im = ax.imshow(hk_radiance_clean, cmap=cmap, vmin=0, vmax=50)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.05)
        cbar.set_label('Radiance (nW/cm²/sr)', fontsize=10)
        
        # Add title
        ax.set_title(f'Hong Kong Night Lights\n{year}-{month}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude', fontsize=10)
        ax.set_ylabel('Latitude', fontsize=10)
        
        # Add grid lines
        ax.grid(False)
        
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add border
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(1)
        
        # Save image
        output_path = os.path.join(output_dir, f"nightlights_{year}_{month}.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='black')
        plt.close()
        
        print(f"  Saved: {output_path}")

print(f"\nDone! Images saved to {output_dir}")