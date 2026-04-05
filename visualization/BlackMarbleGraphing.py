import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

data_dir = "data/raw/BlackMarbleMonthly21-26feb"
files = sorted([f for f in os.listdir(data_dir) if f.endswith('.h5')])

if len(files) == 0:
    print("No files found. Run the download script first.")
    exit()

# Pick first file
file_path = os.path.join(data_dir, files[0])
print(f"Opening: {files[0]}")

with h5py.File(file_path, 'r') as f:
    # Get radiance data
    radiance = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free'][:]
    
    # Get lat/lon grids
    lat = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lat'][:]
    lon = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lon'][:]
    
    print(f"Latitude range: {lat.min():.2f} to {lat.max():.2f}")
    print(f"Longitude range: {lon.min():.2f} to {lon.max():.2f}")
    
    # Hong Kong bounding box (adjusted for h28v07 which covers 110-120°E)
    lat_min, lat_max = 22.0, 22.6
    lon_min, lon_max = 113.7, 114.4
    
    lat_idx = np.where((lat >= lat_min) & (lat <= lat_max))[0]
    lon_idx = np.where((lon >= lon_min) & (lon <= lon_max))[0]
    
    print(f"Latitude indices found: {len(lat_idx)}")
    print(f"Longitude indices found: {len(lon_idx)}")
    
    if len(lat_idx) == 0 or len(lon_idx) == 0:
        print("ERROR: Hong Kong coordinates not in this tile.")
        print(f"Tile covers lon {lon.min():.1f} to {lon.max():.1f}")
        print(f"HK needs lon 113.7 to 114.4")
        exit()
    
    # Extract HK region
    hk_radiance = radiance[np.ix_(lat_idx, lon_idx)]
    
    print(f"\nFile: {files[0]}")
    print(f"Full radiance shape: {radiance.shape}")
    print(f"HK radiance shape: {hk_radiance.shape}")
    print(f"Min radiance: {np.min(hk_radiance):.2f}")
    print(f"Max radiance: {np.max(hk_radiance):.2f}")
    print(f"Mean radiance: {np.mean(hk_radiance):.2f}")
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Full tile
    im1 = axes[0].imshow(radiance, cmap='viridis', vmin=0, vmax=100)
    axes[0].set_title(f'Full Tile - {files[0][:20]}')
    axes[0].set_xlabel('Pixel')
    axes[0].set_ylabel('Pixel')
    plt.colorbar(im1, ax=axes[0], label='Radiance (nW/cm²/sr)')
    
    # Hong Kong zoom
    im2 = axes[1].imshow(hk_radiance, cmap='viridis', vmin=0, vmax=100)
    axes[1].set_title(f'Hong Kong Region - {files[0][:20]}')
    axes[1].set_xlabel('Pixel')
    axes[1].set_ylabel('Pixel')
    plt.colorbar(im2, ax=axes[1], label='Radiance (nW/cm²/sr)')
    
    plt.tight_layout()
    plt.show()
    
    # Print quick stats for the first few months
    print("\n" + "="*50)
    print("Monthly average radiance for HK:")
    print("="*50)
    
    for i, fname in enumerate(files[:12]):  # First 12 months
        file_path = os.path.join(data_dir, fname)
        with h5py.File(file_path, 'r') as f2:
            rad = f2['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free'][:]
            hk_rad = rad[np.ix_(lat_idx, lon_idx)]
            mean_val = np.mean(hk_rad)
            print(f"{fname}: {mean_val:.2f}")