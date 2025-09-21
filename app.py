import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px

# --- Ambil data GeoJSON dari GitHub ---
user = "satriarahman16"
repo = "kotageojson"
pyfile = "Indonesia_cities.geojson"

url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{pyfile}"
response = requests.get(url)
data = response.json()

# --- Filter hanya Papua, Papua Barat, Maluku ---
data["features"] = [
    x for x in data["features"]
    if x["properties"]["NAME_1"] in ["Papua", "Papua Barat", "Maluku"]
]

# --- Buat DataFrame nama kota ---
df_nama_kota = [x["properties"]["NAME_2"] for x in data["features"]]
df = pd.DataFrame(df_nama_kota, columns=['Kota'])

# Tambahkan populasi random per tahun (2021 - 2025)
np.random.seed(42)
for tahun in range(2021, 2026):
    df[str(tahun)] = np.random.randint(50000, 500000, size=len(df))

# Ubah ke format long untuk animasi
df_long = df.melt(
    id_vars=["Kota"], 
    value_vars=[str(t) for t in range(2021, 2026)],
    var_name="Tahun", 
    value_name="Populasi"
)

# --- Plot choropleth dengan animasi ---
fig = px.choropleth(
    df_long,
    geojson=data,
    color="Populasi",
    locations="Kota",
    featureidkey="properties.NAME_2",
    projection="stereographic",
    animation_frame="Tahun",
    color_continuous_scale="Blues",
    labels={"Populasi": "Jumlah Populasi"}
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor="rgba(0,0,0,0)"
)

# Geser posisi slider & play button ke atas peta
for step in fig.layout.sliders:
    step.update(y=1.05)  # geser slider ke atas
for btn in fig.layout.updatemenus:
    btn.update(y=1.15)   # geser tombol play ke atas

fig.update_layout(
    width=1000,
    height=700,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# --- Tampilkan di Streamlit ---
st.header("Visualisasi Populasi pada Kota/Kabupaten di Provinsi Papua, Papua Barat, dan Maluku (2021–2025)")
st.plotly_chart(fig, use_container_width=True)
