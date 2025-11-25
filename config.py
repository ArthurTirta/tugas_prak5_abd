# config.py - Kumpulan fungsi query PostgreSQL
# ======================================================
# File ini berisi:
# 1. Koneksi ke database
# 2. Fungsi untuk mengambil data
# ======================================================

import pandas as pd
import streamlit as st
from supabase import Client, create_client


@st.cache_resource
def init_supabase() -> Client:
    """Inisialisasi koneksi Supabase menggunakan secrets Streamlit."""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    except KeyError as exc:
        raise RuntimeError(
            "Supabase secrets tidak ditemukan. "
            "Pastikan secrets.toml memiliki supabase.url & supabase.key."
        ) from exc
    return create_client(url, key)


supabase = init_supabase()

# -------------------------------
# Query: Ambil semua data produk
# -------------------------------
def get_all_products():
    response = (
        supabase.table("produk")
        .select("id, nama_produk, kategori, harga, stok, latitude, longitude")
        .order("nama_produk", desc=False)
        .execute()
    )
    return pd.DataFrame(response.data)

# -------------------------------
# Query: Ambil total produk per kategori
# -------------------------------
def get_category_count():
    products = get_all_products()
    if products.empty:
        return products
    return (
        products.groupby("kategori", dropna=False)
        .size()
        .reset_index(name="jumlah")
        .sort_values("kategori")
    )

# -------------------------------
# Query: Ambil harga rata-rata per kategori
# -------------------------------
def get_avg_price():
    products = get_all_products()
    if products.empty:
        return products
    return (
        products.groupby("kategori", dropna=False)["harga"]
        .mean()
        .reset_index(name="avg_harga")
        .sort_values("kategori")
    )

# -------------------------------
# Query: Ambil koordinat (latitude & longitude)
# -------------------------------
def get_coordinates():
    products = get_all_products()
    if products.empty:
        return products
    coords = products[["nama_produk", "latitude", "longitude"]].dropna(
        subset=["latitude", "longitude"]
    )
    return coords.reset_index(drop=True)
