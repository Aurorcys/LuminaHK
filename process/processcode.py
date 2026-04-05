import pandas as pd
import numpy as np
import os
import h5py

data_dir = "data/raw"
black_marble_dir = os.path.join(data_dir, "BlackMarbleMonthly21-26feb")
no2_path = os.path.join(data_dir, "airNO2monthly", "air_monthlyNO2|21-25.csv")
gdp_path = os.path.join(data_dir, "hkgdp", "hkgdpquarterly.csv")
air_cargo_path = os.path.join(data_dir, "portactivity", "aircargoactivityannual.csv")
output_path = "data/processed/hk_master_table.csv"

os.makedirs("data/processed", exist_ok=True)

print("Reading NOx data...")
with open(no2_path, 'r') as f:
    lines = f.readlines()

data_lines = []
for i, line in enumerate(lines):
    if i >= 5 and line.strip() and not line.startswith('YEAR,POLLUTANT,STATION'):
        if line.strip() and not line.startswith('Station:') and not line.startswith('Remarks:'):
            data_lines.append(line.strip())

nox_data = []
for line in data_lines:
    parts = line.split(',')
    if len(parts) >= 15 and len(parts) <= 16 and parts[1] == 'Nitrogen Oxides':
        year = int(parts[0])
        if year < 2021:  # Skip 2020
            continue
        station = parts[2]
        months = parts[3:15]
        for month_idx, val in enumerate(months, 1):
            if val != 'N.A.' and val.strip():
                nox_data.append({
                    'year': year,
                    'month': month_idx,
                    'station': station,
                    'nox': float(val)
                })

nox_df = pd.DataFrame(nox_data)

print("Reading GDP data...")
gdp_df = pd.read_csv(gdp_path)
gdp_df = gdp_df[gdp_df['year'] >= 2021]  # Remove 2020

print("Reading Air Cargo data...")
air_cargo_df = pd.read_csv(air_cargo_path)
air_cargo_df = air_cargo_df[air_cargo_df['year'] >= 2021]

print("Processing Black Marble data...")

black_marble_files = [f for f in os.listdir(black_marble_dir) if f.endswith('.h5')]

monthly_radiance = []
hk_lat_idx = None
hk_lon_idx = None

for file_path in black_marble_files:
    parts = file_path.split('_')
    if len(parts) >= 4:
        year = int(parts[2])
        month = int(parts[3])
    else:
        continue
    
    if year < 2021 or year > 2025:
        continue
    
    full_path = os.path.join(black_marble_dir, file_path)
    
    try:
        with h5py.File(full_path, 'r') as f:
            lat = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lat'][:]
            lon = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/lon'][:]
            
            if hk_lat_idx is None:
                lat_min, lat_max = 22.0, 22.6
                lon_min, lon_max = 113.7, 114.4
                hk_lat_idx = np.where((lat >= lat_min) & (lat <= lat_max))[0]
                hk_lon_idx = np.where((lon >= lon_min) & (lon <= lon_max))[0]
            
            radiance = f['HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/AllAngle_Composite_Snow_Free'][:]
            hk_radiance = radiance[np.ix_(hk_lat_idx, hk_lon_idx)]
            
            # Filter out fill values (NASA uses negative values for no data)
            hk_radiance_valid = hk_radiance[hk_radiance >= 0]
            
            if len(hk_radiance_valid) > 0:
                monthly_radiance.append({
                    'year': year,
                    'month': month,
                    'night_light_mean': np.mean(hk_radiance_valid),
                    'night_light_median': np.median(hk_radiance_valid),
                    'night_light_max': np.max(hk_radiance_valid)
                })
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

lights_df = pd.DataFrame(monthly_radiance)

print("Creating quarterly aggregates...")

lights_df['quarter'] = lights_df['month'].apply(lambda x: f"Q{(x-1)//3 + 1}")
lights_quarterly = lights_df.groupby(['year', 'quarter']).agg({
    'night_light_mean': 'mean',
    'night_light_median': 'mean',
    'night_light_max': 'max'
}).reset_index()

nox_df['quarter'] = nox_df['month'].apply(lambda x: f"Q{(x-1)//3 + 1}")
nox_quarterly = nox_df.groupby(['year', 'quarter', 'station'])['nox'].mean().reset_index()
nox_quarterly_pivot = nox_quarterly.pivot_table(index=['year', 'quarter'], columns='station', values='nox').reset_index()
nox_quarterly_pivot.columns = ['year', 'quarter'] + [col.lower().replace(' ', '_').replace('/', '_') for col in nox_quarterly_pivot.columns[2:]]

print("Merging all data...")

master = gdp_df.copy()
master = master.merge(lights_quarterly, on=['year', 'quarter'], how='left')
master = master.merge(nox_quarterly_pivot, on=['year', 'quarter'], how='left')

# Add air cargo data (annual, so repeat for each quarter)
air_cargo_expanded = []
for _, row in air_cargo_df.iterrows():
    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        air_cargo_expanded.append({
            'year': row['year'],
            'quarter': quarter,
            'air_cargo_thousand_teu': row['air_cargo_thousand_teu'],
            'air_cargo_yoy_pct': row['air_cargo_yoy_pct']
        })
air_cargo_expanded_df = pd.DataFrame(air_cargo_expanded)

master = master.merge(air_cargo_expanded_df, on=['year', 'quarter'], how='left')

master = master.sort_values(['year', 'quarter'])

master.to_csv(output_path, index=False)
print(f"Master table saved to: {output_path}")
print(f"Shape: {master.shape}")
print("\nFirst 5 rows:")
print(master.head())
print("\nColumn names:")
print(master.columns.tolist())

# Quick correlation check (2021-2025 only)
print("\n" + "="*50)
print("Correlation with GDP Growth (2021-2025):")
print("="*50)
print(f"Night Light Mean vs GDP: {master['night_light_mean'].corr(master['gdp_growth_yoy_pct']):.3f}")
print(f"Causeway Bay NOx vs GDP: {master['causeway_bay'].corr(master['gdp_growth_yoy_pct']):.3f}")
print(f"Air Cargo YoY vs GDP: {master['air_cargo_yoy_pct'].corr(master['gdp_growth_yoy_pct']):.3f}")
print(f"Night Light vs Causeway Bay NOx: {master['night_light_mean'].corr(master['causeway_bay']):.3f}")