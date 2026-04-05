import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# Path to your Black Marble files
data_dir = "data/raw/BlackMarbleMonthly22-26feb"

# List all files
files = os.listdir(data_dir)
print("Files found:")
for f in sorted(files)[:5]:
    print(f"  {f}")

# Pick first file
file_path = os.path.join(data_dir, files[0])
print(f"\nOpening: {file_path}")

# Inspect file structure
with h5py.File(file_path, 'r') as f:
    print("\n" + "=" * 50)
    print("Keys in file:")
    print("=" * 50)
    for key in f.keys():
        print(f"  {key}")
    
    # Recursively print all groups/datasets
    def print_all(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"  {name}: shape={obj.shape}, dtype={obj.dtype}")
        else:
            print(f"  {name}/")
    
    print("\nFull structure:")
    f.visititems(print_all)


"""
OUTPUT:
==================================================
Keys in file:
==================================================
  HDFEOS
  HDFEOS INFORMATION

Full structure:
  HDFEOS/
  HDFEOS/ADDITIONAL/
  HDFEOS/ADDITIONAL/FILE_ATTRIBUTES/
  HDFEOS/GRIDS/
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Covered: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Covered_Num: shape=(2400, 2400), dtype=uint16
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Covered_Quality: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Covered_Std: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free_Num: shape=(2400, 2400), dtype=uint16
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free_Quality: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free_Std: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/DNB_Platform: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/Land_Water_Mask: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Covered: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Covered_Num: shape=(2400, 2400), dtype=uint16
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Covered_Quality: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Covered_Std: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free_Num: shape=(2400, 2400), dtype=uint16
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free_Quality: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/NearNadir_Composite_Snow_Free_Std: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Covered: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Covered_Num: shape=(2400, 2400), dtype=uint16
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Covered_Quality: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Covered_Std: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Free: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Free_Num: shape=(2400, 2400), dtype=uint16
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Free_Quality: shape=(2400, 2400), dtype=uint8
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/OffNadir_Composite_Snow_Free_Std: shape=(2400, 2400), dtype=float32
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lat: shape=(2400,), dtype=float64
  HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lon: shape=(2400,), dtype=float64
  HDFEOS INFORMATION/
  HDFEOS INFORMATION/StructMetadata.0: shape=(), dtype=|S32000
"""