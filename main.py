# main.py - Visualisasi Streamlit
# ======================================================
# Menampilkan dropdown pilihan chart (Pie, Bar, Line, Area, Map)
# Mengambil data dari config.py
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import config

st.set_page_config(page_title="Visualisasi Produk", page_icon="📊", layout="wide")

st.title("📊 Visualisasi Data Produk Elektronik")
st.write("Berikut adalah beberapa visualisasi sederhana berdasarkan 15 data produk.")

# Ambil data
products = config.get_all_products()
category_count = config.get_category_count()
avg_price = config.get_avg_price()
coords = config.get_coordinates()

st.sidebar.title("📑 Navigation Menu")
st.sidebar.markdown("---")

# Dropdown
option = st.sidebar.radio(
    "Pilih jenis visualisasi:",
    ["Pie Chart - Jumlah Produk per Kategori",
     "Bar Chart - Harga Rata-rata per Kategori",
     "Line Chart - Stok tiap Produk",
     "Area Chart - Harga tiap Produk",
     "Map - Lokasi Produk"]
)

# ===================== PIE CHART =====================
if option == "Pie Chart - Jumlah Produk per Kategori":
    st.subheader("Persentase Produk per Kategori")
    st.write("Visualisasi ini menunjukkan distribusi jumlah produk berdasarkan kategori.")

    import plotly.express as px
    fig = px.pie(category_count, names='kategori', values='jumlah', title='Distribusi Produk per Kategori')
    st.plotly_chart(fig)

# ===================== BAR CHART ===================== - Harga Rata-rata per Kategori":
elif option == "Bar Chart - Harga Rata-rata per Kategori":
    st.subheader("Harga Rata-rata per Kategori")
    st.bar_chart(avg_price, x="kategori", y="avg_harga")
    st.write("Grafik batang ini memperlihatkan perbandingan harga rata-rata tiap kategori.")

# ===================== LINE CHART =====================
elif option == "Line Chart - Stok tiap Produk":
    st.subheader("Pergerakan Stok Produk")
    st.line_chart(products, x="nama_produk", y="stok")
    st.write("Line chart menunjukkan jumlah stok tiap produk secara berurutan.")

# ===================== AREA CHART =====================
elif option == "Area Chart - Harga tiap Produk":
    st.subheader("Area Chart Harga Produk")
    st.area_chart(products, x="nama_produk", y="harga")
    st.write("Area chart ini menggambarkan perbedaan harga antar produk.")

# ===================== MAP =====================
elif option == "Map - Lokasi Produk":
    st.map(coords.rename(columns={"latitude": "lat", "longitude": "lon"}))
    st.write("Peta ini menampilkan lokasi penyimpanan produk berdasarkan koordinat.")
