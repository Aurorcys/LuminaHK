import h5py
import numpy as np
import os

data_dir = "tests"
files = sorted([f for f in os.listdir(data_dir) if f.endswith('.h5')])

file_path = os.path.join(data_dir, files[0])

with h5py.File(file_path, 'r') as f:
    lat = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lat'][:]
    lon = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lon'][:]
    
    print(f"Latitude range: {lat.min():.2f} to {lat.max():.2f}")
    print(f"Longitude range: {lon.min():.2f} to {lon.max():.2f}")
    print(f"Latitude shape: {lat.shape}")
    print(f"Longitude shape: {lon.shape}")
    print(f"\nFirst 10 lat values: {lat[:10]}")
    print(f"First 10 lon values: {lon[:10]}")

"""
OUTPUT:

Latitude range: 20.00 to 30.00
Longitude range: 110.00 to 120.00
Latitude shape: (2400,)
Longitude shape: (2400,)

First 10 lat values: [30.         29.99583333 29.99166667 29.9875     29.98333333 29.97916667
 29.975      29.97083333 29.96666667 29.9625    ]
First 10 lon values: [110.         110.00416667 110.00833333 110.0125     110.01666667
 110.02083333 110.025      110.02916667 110.03333333 110.0375    ]

As HK is around 114°E, 22°N, this is perfect for us
"""