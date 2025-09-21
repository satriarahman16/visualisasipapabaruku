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

# Tambahkan populasi random per tahun
np.random.seed(42)  # supaya hasilnya konsisten setiap run
df['2023'] = np.random.randint(50000, 500000, size=len(df))
df['2024'] = np.random.randint(50000, 500000, size=len(df))
df['2025'] = np.random.randint(50000, 500000, size=len(df))

st.title("Visualisasi Kota di Papua, Papua Barat, dan Maluku")

# --- Pilihan interaktif tahun ---
tahun = st.radio(
    "Pilih Tahun Populasi:",
    options=['2023', '2024', '2025'],
    horizontal=True
)

# --- Plot choropleth sesuai tahun yang dipilih ---
fig = px.choropleth(
    df,
    geojson=data,
    color=tahun,
    locations="Kota",
    featureidkey="properties.NAME_2",
    projection="stereographic",
    color_continuous_scale="Blues",  # bisa ganti colormap
    labels={tahun: f"Populasi {tahun}"}
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor="rgba(0,0,0,0)"
)

fig.update_layout(
    width=1000,
    height=700,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    transition = {"duration": 1000, "easing": "cubic-in-out"} 
)

# --- Tampilkan di Streamlit ---

st.plotly_chart(fig, use_container_width=True)
