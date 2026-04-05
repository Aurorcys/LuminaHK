import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/processed/hk_master_table.csv")

df['date'] = pd.to_datetime(df['year'].astype(str) + df['quarter'].str.replace('Q', '-Q'))

# Filter out 2020
df = df[df['year'] >= 2021].copy()

# Get annual data for GDP and Air Cargo only
annual_df = df[df['quarter'] == 'Q1'].copy()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Night lights over time (quarterly)
ax1 = axes[0, 0]
ax1.plot(df['date'], df['night_light_mean'], 'o-', color='blue', linewidth=1.5, markersize=3)
ax1.set_title('Night Lights Over Time (Quarterly)')
ax1.set_ylabel('Mean Radiance (nW/cm²/sr)')
ax1.set_xlabel('Year')
ax1.grid(True, alpha=0.3)

# Plot 2: GDP growth vs Air Cargo (both annual)
ax2 = axes[0, 1]
ax2.plot(annual_df['year'], annual_df['gdp_growth_yoy_pct'], 'o-', color='green', linewidth=2, markersize=8, label='GDP Growth')
ax2.plot(annual_df['year'], annual_df['air_cargo_yoy_pct'], 's-', color='orange', linewidth=2, markersize=8, label='Air Cargo Growth')
ax2.set_ylabel('Growth Rate (%)', fontsize=11)
ax2.set_title('GDP Growth vs Air Cargo Growth (Annual)')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='best')
ax2.set_ylim(-20, 20)
ax2.set_xticks(annual_df['year'])
ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

# Plot 3: NOx trends by top stations (quarterly)
ax3 = axes[1, 0]
stations = ['causeway_bay', 'central', 'mong_kok', 'kwun_tong', 'tuen_mun']
for station in stations:
    if station in df.columns:
        ax3.plot(df['date'], df[station], 'o-', label=station.replace('_', ' ').title(), linewidth=1.5, markersize=3)
ax3.set_title('NOx Trends by Station (Quarterly)')
ax3.set_ylabel('NOx (μg/m³)')
ax3.set_xlabel('Year')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# Plot 4: Air Cargo vs GDP scatter (annual)
ax4 = axes[1, 1]
ax4.scatter(annual_df['air_cargo_yoy_pct'], annual_df['gdp_growth_yoy_pct'], alpha=0.8, s=120, c='darkgreen')

# Add year labels to points
for _, row in annual_df.iterrows():
    ax4.annotate(int(row['year']), (row['air_cargo_yoy_pct'], row['gdp_growth_yoy_pct']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)

ax4.set_xlabel('Air Cargo Growth (%)')
ax4.set_ylabel('GDP Growth (%)')
ax4.set_title('Air Cargo vs GDP Growth (Annual)')
ax4.grid(True, alpha=0.3)
ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax4.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

# Add trend line
z = np.polyfit(annual_df['air_cargo_yoy_pct'], annual_df['gdp_growth_yoy_pct'], 1)
p = np.poly1d(z)
r2 = np.corrcoef(annual_df['air_cargo_yoy_pct'], annual_df['gdp_growth_yoy_pct'])[0,1]**2
x_line = np.array([-20, 20])
ax4.plot(x_line, p(x_line), "r--", alpha=0.8, label=f'R² = {r2:.2f}')
ax4.legend()
ax4.set_xlim(-20, 20)
ax4.set_ylim(-5, 15)

plt.tight_layout()
plt.savefig("data/processed/lumina_plots.png", dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "="*50)
print("Correlation Summary (2021-2025):")
print("="*50)
print(f"Night Light Mean vs GDP: {df['night_light_mean'].corr(df['gdp_growth_yoy_pct']):.3f}")
print(f"Causeway Bay NOx vs GDP: {df['causeway_bay'].corr(df['gdp_growth_yoy_pct']):.3f}")
print(f"Air Cargo YoY vs GDP: {annual_df['air_cargo_yoy_pct'].corr(annual_df['gdp_growth_yoy_pct']):.3f}")
print(f"Night Light vs Causeway Bay NOx: {df['night_light_mean'].corr(df['causeway_bay']):.3f}")


"""
OUTPUT
==================================================
Correlation Summary (2021-2025):
==================================================
Night Light Mean vs GDP: 0.012
Causeway Bay NOx vs GDP: 0.279
Air Cargo YoY vs GDP: 0.884
Night Light vs Causeway Bay NOx: 0.329
cyrus@Onnas-iMac LuminaHKv1 % 
"""