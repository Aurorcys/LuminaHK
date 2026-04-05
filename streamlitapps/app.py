import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import os
import glob

st.set_page_config(page_title="LuminaHK", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #ffffff, #8888ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #8888aa;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .about-box {
        text-align: center;
        background: linear-gradient(135deg, #1a1a3a, #0a0a2a);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid #4a4a8a;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e3a, #0d0d2a);
        padding: 15px;
        border-radius: 12px;
        border-left: 3px solid #ff4a2a;
    }
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4a4a8a, transparent);
    }
    .stButton button {
        background: linear-gradient(135deg, #2a2a4a, #1a1a3a);
        border: 1px solid #4a4a8a;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #3a3a5a, #2a2a4a);
        border-color: #ff4a2a;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Title and About section
st.markdown('<div class="main-title">LUMINAHK</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Seeing Hong Kong\'s Economy from Space</div>', unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
    <b>🛰️ Tracking Hong Kong's economic pulse using space-derived data</b><br>
    NASA Black Marble night lights | Sentinel-5P NOx pollution | ADS-B air cargo tracking
    <br><br>
    <b>Key Finding:</b> Air Cargo vs GDP correlation = <b style="color:#ffaa44;">R² = 0.845</b>
</div>
""", unsafe_allow_html=True)

# Load master data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/hk_master_table.csv")
    df['date'] = pd.to_datetime(df['year'].astype(str) + df['quarter'].str.replace('Q', '-Q'))
    return df

df = load_data()
annual_df = df[df['quarter'] == 'Q1'].copy()

# Get list of available night lights images
@st.cache_data
def get_available_images():
    image_dir = "data/processed/images(streamlit)"
    images = glob.glob(os.path.join(image_dir, "nightlights_*.png"))
    image_data = []
    for img_path in images:
        basename = os.path.basename(img_path)
        parts = basename.replace('nightlights_', '').replace('.png', '').split('_')
        if len(parts) >= 2:
            year = int(parts[0])
            month = int(parts[1])
            image_data.append({
                'year': year,
                'month': month,
                'path': img_path,
                'label': f"{year}-{month:02d}"
            })
    return sorted(image_data, key=lambda x: (x['year'], x['month']))

images = get_available_images()

# Initialize session state
if 'img_index' not in st.session_state:
    st.session_state.img_index = len(images) - 1 if images else 0

# Define five districts
districts = {
    'causeway_bay': 'Causeway Bay',
    'central': 'Central',
    'mong_kok': 'Mong Kok',
    'kwun_tong': 'Kwun Tong',
    'tuen_mun': 'Tuen Mun'
}

# Calculate annual average NOx
nox_annual = df.groupby('year')[list(districts.keys())].mean().reset_index()

# Get current image info
if images:
    current_img = images[st.session_state.img_index]
    selected_year = current_img['year']
    selected_month = current_img['month']
else:
    selected_year = 2022
    selected_month = 1

# Row 1: Black Marble (left) + Key Metrics & Air Cargo (right)
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("Night Lights")
    
    if images:
        with st.spinner("Loading night lights..."):
            img = Image.open(current_img['path'])
            st.image(img, use_container_width=True)
        
        # Slider directly under image
        img_index = st.slider(
            "Timeline",
            0,
            len(images) - 1,
            st.session_state.img_index,
            format="%d",
            key="img_slider",
            label_visibility="collapsed"
        )
        
        if img_index != st.session_state.img_index:
            st.session_state.img_index = img_index
            st.rerun()
        
        st.caption(f"**{current_img['label']}** | Image {st.session_state.img_index + 1} of {len(images)} | *Drag to explore time series*")
    else:
        st.warning("No night lights images found")

with row1_col2:
    st.subheader("Key Metrics")
    
    relevant_data = annual_df[annual_df['year'] <= selected_year]
    if not relevant_data.empty:
        latest = relevant_data[relevant_data['year'] == relevant_data['year'].max()]
        if not latest.empty:
            st.metric("GDP Growth", f"{latest['gdp_growth_yoy_pct'].values[0]:.1f}%")
            air_cargo_row = annual_df[annual_df['year'] == latest['year'].values[0]]
            if not air_cargo_row.empty:
                st.metric("Air Cargo Growth", f"{air_cargo_row['air_cargo_yoy_pct'].values[0]:.1f}%")
    
    st.subheader("Air Cargo vs GDP")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=annual_df['year'], y=annual_df['gdp_growth_yoy_pct'],
                             mode='lines+markers', name='GDP Growth', line=dict(color='green', width=3),
                             marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=annual_df['year'], y=annual_df['air_cargo_yoy_pct'],
                             mode='lines+markers', name='Air Cargo Growth', line=dict(color='orange', width=3),
                             marker=dict(size=10)))
    
    # COVID impact shading
    fig.add_vrect(x0=2022, x1=2022.5, 
                  fillcolor="red", opacity=0.15, 
                  layer="below", line_width=0,
                  annotation_text="COVID Fifth Wave",
                  annotation_position="top left",
                  annotation_font_size=10)
    
    fig.add_vline(x=selected_year, line_dash="dash", line_color="red", line_width=2,
                  annotation_text=f"{selected_year}", annotation_position="top right")
    
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Row 2: COVID Impact (bottom left) + NOx vs GDP (bottom right)
row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.subheader("📉 COVID Impact (2022)")
    
    covid_impact = annual_df[annual_df['year'] == 2022]
    if not covid_impact.empty:
        gdp_drop = covid_impact['gdp_growth_yoy_pct'].mean()
        air_drop = covid_impact['air_cargo_yoy_pct'].mean()
        
        col_covid1, col_covid2 = st.columns(2)
        col_covid1.metric("GDP Change", f"{gdp_drop:.1f}%", "-3.5% avg", delta_color="inverse")
        col_covid2.metric("Air Cargo Change", f"{air_drop:.1f}%", "-16.4% peak", delta_color="inverse")
        
        st.caption("Fifth wave and border closures caused sharp contraction. Recovery began Q3 2022.")
    
    # District Ranking Section
    st.subheader("🏆 District Ranking")
    
    # Calculate latest year NOx values
    latest_year = nox_annual['year'].max()
    latest_nox = nox_annual[nox_annual['year'] == latest_year].iloc[0]
    
    # Calculate correlation for each district
    ranking_data = []
    for district, name in districts.items():
        district_corr = nox_annual[['year', district]].merge(annual_df[['year', 'gdp_growth_yoy_pct']], on='year')
        district_corr = district_corr.dropna()
        corr_val = district_corr[district].corr(district_corr['gdp_growth_yoy_pct'])
        ranking_data.append({
            'District': name,
            'NOx Level': latest_nox[district],
            'Correlation with GDP': corr_val
        })
    
    ranking_df = pd.DataFrame(ranking_data)
    ranking_df = ranking_df.sort_values('NOx Level', ascending=False)
    
    # Display ranking with medals
    col_rank1, col_rank2, col_rank3 = st.columns(3)
    
    medals = ['🥇', '🥈', '🥉']
    for i, (_, row) in enumerate(ranking_df.head(3).iterrows()):
        with [col_rank1, col_rank2, col_rank3][i]:
            st.metric(
                f"{medals[i]} {row['District']}",
                f"{row['NOx Level']:.0f} μg/m³",
                f"R² = {row['Correlation with GDP']:.2f}"
            )
    
    # Show full ranking table
    with st.expander("View Full District Rankings"):
        st.dataframe(
            ranking_df.style.format({
                'NOx Level': '{:.0f}',
                'Correlation with GDP': '{:.3f}'
            }).bar(subset=['NOx Level'], color='#ff4a2a', vmin=0, vmax=250),
            use_container_width=True
        )
        st.caption("Higher NOx indicates more traffic/industrial activity")

with row2_col2:
    st.subheader("NOx vs GDP by District")
    
    # District buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    col_btn4, col_btn5 = st.columns(2)
    
    selected_district = None
    
    with col_btn1:
        if st.button("Causeway Bay", use_container_width=True):
            selected_district = 'causeway_bay'
    with col_btn2:
        if st.button("Central", use_container_width=True):
            selected_district = 'central'
    with col_btn3:
        if st.button("Mong Kok", use_container_width=True):
            selected_district = 'mong_kok'
    with col_btn4:
        if st.button("Kwun Tong", use_container_width=True):
            selected_district = 'kwun_tong'
    with col_btn5:
        if st.button("Tuen Mun", use_container_width=True):
            selected_district = 'tuen_mun'
    
    if selected_district is None:
        selected_district = 'causeway_bay'
        st.info("Causeway Bay selected")
    
    district_col = selected_district
    district_display = districts[selected_district]
    
    corr_df = nox_annual[['year', district_col]].merge(annual_df[['year', 'gdp_growth_yoy_pct']], on='year')
    corr_df = corr_df.dropna()
    correlation = corr_df[district_col].corr(corr_df['gdp_growth_yoy_pct'])
    r2 = correlation ** 2
    
    col_metric1, col_metric2 = st.columns(2)
    col_metric1.metric("Correlation (r)", f"{correlation:.3f}")
    col_metric2.metric("R-squared", f"{r2:.3f}")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=corr_df['year'], y=corr_df[district_col],
                              mode='lines+markers', 
                              name=f'{district_display} NOx',
                              line=dict(color='purple', width=2),
                              marker=dict(size=8),
                              yaxis="y1"))
    fig2.add_trace(go.Scatter(x=corr_df['year'], y=corr_df['gdp_growth_yoy_pct'],
                              mode='lines+markers', 
                              name='GDP Growth',
                              line=dict(color='green', width=2, dash='dash'),
                              marker=dict(size=8),
                              yaxis="y2"))
    
    # COVID impact shading
    fig2.add_vrect(x0=2022, x1=2022.5, 
                   fillcolor="red", opacity=0.15, 
                   layer="below", line_width=0)
    
    fig2.add_vline(x=selected_year, line_dash="dash", line_color="red")
    fig2.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(title=f"{district_display} NOx (μg/m³)", tickfont=dict(color='purple'), side='left'),
        yaxis2=dict(title="GDP Growth (%)", tickfont=dict(color='green'), side='right', overlaying='y', anchor='x'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig2, use_container_width=True)

# Correlation Heatmap Section - Fixed Size
st.divider()
st.subheader("Correlation Heatmap")

with st.expander("Customize Heatmap", expanded=False):
    col_heat1, col_heat2 = st.columns(2)
    
    with col_heat1:
        available_vars = {
            'gdp_growth_yoy_pct': 'GDP Growth',
            'air_cargo_yoy_pct': 'Air Cargo',
            'causeway_bay': 'Causeway Bay NOx',
            'central': 'Central NOx',
            'mong_kok': 'Mong Kok NOx',
            'kwun_tong': 'Kwun Tong NOx',
            'tuen_mun': 'Tuen Mun NOx',
            'night_light_mean': 'Night Lights'
        }
        selected_vars = st.multiselect(
            "Select variables to include",
            options=list(available_vars.keys()),
            default=['gdp_growth_yoy_pct', 'air_cargo_yoy_pct', 'causeway_bay', 'night_light_mean'],
            format_func=lambda x: available_vars[x],
            key="heatmap_vars"
        )
    
    with col_heat2:
        color_scale = st.selectbox(
            "Color scale",
            ['RdBu', 'Viridis', 'Plasma', 'Cividis', 'Blues', 'Reds'],
            index=0,
            key="heatmap_colorscale"
        )
        show_values = st.checkbox("Show correlation values", value=True, key="heatmap_showvals")

if len(selected_vars) >= 2:
    data_frames = []
    data_frames.append(annual_df[['year', 'gdp_growth_yoy_pct']])
    
    if 'air_cargo_yoy_pct' in selected_vars:
        data_frames.append(annual_df[['year', 'air_cargo_yoy_pct']])
    
    if 'night_light_mean' in selected_vars:
        night_lights_annual = df.groupby('year')['night_light_mean'].mean().reset_index()
        data_frames.append(night_lights_annual)
    
    nox_stations = [s for s in selected_vars if s in districts.keys()]
    if nox_stations:
        nox_annual_temp = df.groupby('year')[nox_stations].mean().reset_index()
        data_frames.append(nox_annual_temp)
    
    heatmap_data = data_frames[0]
    for df_temp in data_frames[1:]:
        heatmap_data = heatmap_data.merge(df_temp, on='year')
    
    corr_matrix = heatmap_data.drop(columns=['year']).corr()
    rename_map = {k: v for k, v in available_vars.items() if k in corr_matrix.columns}
    corr_matrix = corr_matrix.rename(columns=rename_map, index=rename_map)
    
    # FIXED SIZE - 800x800 pixels, no dynamic scaling
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale=color_scale,
        zmin=-1 if color_scale == 'RdBu' else None,
        zmax=1 if color_scale == 'RdBu' else None,
        text=corr_matrix.values.round(2) if show_values else None,
        texttemplate='%{text}' if show_values else None,
        textfont={"size": 14},
        hoverongaps=False
    ))
    
    fig_heatmap.update_layout(
        height=700,
        width=700,
        xaxis_title="",
        yaxis_title="",
        xaxis={'side': 'bottom', 'tickangle': 45, 'tickfont': {'size': 12}},
        yaxis={'side': 'left', 'tickfont': {'size': 12}},
        autosize=False,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    # Center the heatmap
    left_col, center_col, right_col = st.columns([1, 2, 1])
    with center_col:
        st.plotly_chart(fig_heatmap, use_container_width=False)
    
    # Display top correlations with GDP
    if 'GDP Growth' in corr_matrix.columns:
        st.subheader("Top Correlations with GDP")
        corr_with_gdp = corr_matrix['GDP Growth'].drop('GDP Growth').sort_values(ascending=False)
        
        cols = st.columns(min(3, len(corr_with_gdp)))
        for i, (var, corr_val) in enumerate(corr_with_gdp.head(3).items()):
            with cols[i]:
                strength = "Strong" if abs(corr_val) > 0.7 else "Moderate" if abs(corr_val) > 0.3 else "Weak"
                st.metric(f"vs {var}", f"{corr_val:.3f}", strength)
else:
    st.warning("Select at least 2 variables to display heatmap")

# Three explanation boxes at the bottom
st.divider()
st.subheader("Understanding the Correlations")

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a3a1a, #0a2a0a); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #00ff00; height: 100%;">
        <h3 style="margin-top: 0; color: #00ff00;">📦 Air Cargo</h3>
        <p style="font-size: 1.1rem; font-weight: bold;">R² = 0.845 <span style="color: #00ff00;">(Strong)</span></p>
        <p><b>Why it works:</b> During 2021-2025, Hong Kong saw increased demand for high-value electronic goods (semiconductors, mobile phones, luxury items). These are primarily shipped via air freight, making air cargo volume a direct proxy for trade value and GDP growth.</p>
        <p><b>Signal quality:</b> Excellent leading indicator. Near real-time via ADS-B satellite aircraft tracking.</p>
        <p><b>Key insight:</b> When tracking an economy, focus on its most valuable trade sectors. For Hong Kong, air cargo captures the high-value electronics trade that drives GDP.</p>
    </div>
    """, unsafe_allow_html=True)

with col_exp2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a3a, #0a0a2a); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #aa44ff; height: 100%;">
        <h3 style="margin-top: 0; color: #aa44ff;">🌫️ NOx Pollution</h3>
        <p style="font-size: 1.1rem; font-weight: bold;">R² = 0.279 <span style="color: #ffaa44;">(Moderate)</span></p>
        <p><b>Why it works:</b> NOx comes from combustion - vehicles, power plants, industry. Tracks traffic density and industrial activity. Causeway Bay (high traffic) shows stronger correlation.</p>
        <p><b>Signal quality:</b> Good ground truth for urban activity. Limited by weather patterns and Hong Kong's transition to cleaner energy.</p>
        <p><b>Key insight:</b> Best used as a supporting indicator for traffic and industrial trends, not a standalone GDP proxy.</p>
    </div>
    """, unsafe_allow_html=True)

with col_exp3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3a1a1a, #2a0a0a); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ff4444; height: 100%;">
        <h3 style="margin-top: 0; color: #ff4444;">💡 Night Lights (Black Marble)</h3>
        <p style="font-size: 1.1rem; font-weight: bold;">R² = 0.012 <span style="color: #ff4444;">(Weak)</span></p>
        <p><b>Why it fails:</b> The VIIRS sensor saturates at high radiance levels. Hong Kong's extremely bright urban core exceeds this saturation point, making it impossible to detect meaningful changes in light output. The signal is permanently "maxed out."</p>
        <p><b>Resolution issue:</b> 500m pixels are too coarse for HK's dense vertical city. Each pixel mixes residential, commercial, and industrial light, with no room to capture economic fluctuations.</p>
        <p><b>Key insight:</b> Hong Kong is NOT a suitable location for using Black Marble night lights to predict economic changes. Higher resolution (30m) or different sensors would be needed.</p>
    </div>
    """, unsafe_allow_html=True)

# Conclusion Section
st.divider()
st.subheader("Conclusion: What We Learned")

st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a2a, #0a0a1a); padding: 2rem; border-radius: 12px; border: 1px solid #4a4a8a;">
    <p style="font-size: 1.1rem; line-height: 1.6;">
        <b>1. Air cargo is a powerful economic indicator for Hong Kong.</b> With an R² of 0.845, it captures 
        the high-value electronics trade that drives GDP growth. This demonstrates that space-derived data 
        (ADS-B aircraft tracking) can provide near real-time economic signals before official statistics are released.
    </p>
    <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
        <b>2. One size does not fit all.</b> The weak correlation from night lights proves that different 
        economies require different space-based proxies. Hong Kong's extreme density and brightness saturate 
        the VIIRS sensor. A less dense city might show stronger night lights correlation.
    </p>
    <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
        <b>3. Research the local economy first.</b> When trying to predict economic growth in any region, 
        identify its most valuable and important industries. For Hong Kong, beyond air cargo, potential 
        indicators include:
        <ul style="margin-top: 0.5rem;">
            <li><b>Stock market activity</b> (Hang Seng Index volatility and volume)</li>
            <li><b>Office occupancy rates</b> (via satellite night lights or thermal imaging)</li>
            <li><b>Port container throughput</b> (via satellite AIS ship tracking)</li>
            <li><b>Credit card transaction volumes</b> (via economic reports)</li>
        </ul>
    </p>
    <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem; font-style: italic; border-top: 1px solid #4a4a8a; padding-top: 1rem;">
        <b>LuminaHK's core takeaway:</b> Space data is valuable, but only when matched to the right economic context. 
        Understand your target economy first. Then choose the satellite proxy that fits.
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; padding: 1rem 0; color: #666; font-size: 0.8rem;">
    <span>NASA Black Marble | Copernicus Sentinel-5P | HK Census & Statistics Department</span>
    <br>
    <span>LuminaHK © 2026 — Seeing Hong Kong's Economy from Space</span>
</div>
""", unsafe_allow_html=True)


#streamlit run streamlitapps/app.py
