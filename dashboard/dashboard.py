import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Muat data
script_dir = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(f"{script_dir}/PRSA_Data_Aotizhongxin_20130301-20170228.csv")

# Cek tipe data
print("Tipe Data Sebelum Pembersihan:")
print(data.dtypes)

# Konversi kolom yang seharusnya numerik
kolom_polutan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']  # Hanya mengambil kolom polutan
for col in kolom_polutan:
    # Ubah menjadi numerik, buat nilai non-numerik menjadi NaN
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Cek nilai NaN setelah konversi
print("Jumlah Nilai NaN setelah Pembersihan:")
print(data[kolom_polutan].isna().sum())

# Hapus baris yang memiliki nilai NaN di kolom yang relevan
data.dropna(subset=kolom_polutan, inplace=True)

# Set konfigurasi halaman
st.set_page_config(page_title="Dasbor Analisis Kualitas Udara", layout="wide")

# Judul dashboard
st.title("Dashboard Analisis Kualitas Udara")

# Sidebar untuk filter
st.sidebar.title("Opsi Filter")
selected_month = st.sidebar.selectbox("Pilih Bulan", data['month'].unique())

# Filter hari berdasarkan bulan yang dipilih
filtered_days = data[data['month'] == selected_month]['day'].unique()
selected_day = st.sidebar.selectbox("Pilih Hari", filtered_days)

# Filter data berdasarkan bulan, hari, dan jam yang dipilih
filtered_data = data[(data['month'] == selected_month) & (data['day'] == selected_day)]

# **1. Tren Kualitas Udara di Stasiun Aotizhongxin**
st.subheader("Tren Kualitas Udara di Bulan yang Dipilih")
tren_bulanan = data[data['month'] == selected_month].groupby('day').mean(numeric_only=True).reset_index()

if not tren_bulanan.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(tren_bulanan['day'], tren_bulanan['PM2.5'], label='PM2.5', color='b')
    ax.plot(tren_bulanan['day'], tren_bulanan['PM10'], label='PM10', color='g')
    ax.plot(tren_bulanan['day'], tren_bulanan['SO2'], label='SO2', color='c')
    ax.plot(tren_bulanan['day'], tren_bulanan['NO2'], label='NO2', color='y')
    ax.plot(tren_bulanan['day'], tren_bulanan['O3'], label='O3', color='r')
    ax.set_xlabel("Hari dalam Bulan")
    ax.set_ylabel("Tingkat Polutan")
    ax.set_title(f"Tren Kualitas Udara Bulan Ke-{selected_month} di Stasiun Aotizhongxin")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("Tidak ada data untuk bulan yang dipilih.")

# **2. Korelasi antara Polutan dan Waktu dalam Sehari (DiDibagi dalam 3 Segmen)**
st.subheader("Korelasi antara Polutan dan Waktu dalam Sehari (Per 8 Jam)")

# Filter data berdasarkan bulan dan hari yang dipilih untuk heatmap
filtered_data_by_day = data[(data['month'] == selected_month) & (data['day'] == selected_day)]

# Mengelompokkan data berdasarkan jam dan menghitung rata-rata konsentrasi polutan
rata_rata_per_jam = filtered_data_by_day.groupby('hour').mean(numeric_only=True)

# Membuat heatmap per 8 jam
rentang_waktu = [(0, 7), (8, 15), (16, 23)]  # Membagi hari menjadi 3 bagian masing-masing 8 jam

for start_hour, end_hour in rentang_waktu:
    st.subheader(f"Heatmap untuk Jam {start_hour}:00 - {end_hour}:59")

    segmen_per_jam = rata_rata_per_jam[(rata_rata_per_jam.index >= start_hour) & (rata_rata_per_jam.index <= end_hour)]

    if not segmen_per_jam.empty:
        # Visualisasi heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(segmen_per_jam[kolom_polutan].T, cmap='coolwarm', annot=True, fmt=".2f", ax=ax)
        ax.set_title(f'Korelasi antara Konsentrasi Polutan dan Waktu dalam Sehari (Jam {start_hour} - {end_hour})')
        ax.set_xlabel('Jam dalam Sehari')
        ax.set_ylabel('Jenis Polutan')
        st.pyplot(fig)
    else:
        st.warning(f"Tidak ada data untuk rentang waktu {start_hour}:00 - {end_hour}:59.")
