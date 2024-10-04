import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Muat data
script_dir = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(f"{script_dir}/PRSA_Data_Aotizhongxin_20130301-20170228.csv")

# Konversi kolom yang seharusnya numerik
kolom_polutan = ['SO2', 'NO2', 'CO', 'O3', 'PM2.5', 'PM10']
for col in kolom_polutan:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Hapus baris yang memiliki nilai NaN di kolom yang relevan
data.dropna(subset=kolom_polutan, inplace=True)

# Konversi waktu ke datetime
data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
data.set_index('datetime', inplace=True)

# Set konfigurasi halaman
st.set_page_config(page_title="Dasbor Analisis Kualitas Udara", layout="wide")

# Judul dashboard
st.title("Dashboard Analisis Kualitas Udara di Stasiun Aotizhongxin")

# Sidebar untuk filter
st.sidebar.title("Opsi Filter")

# ---------------------------------------
# Filter untuk Visualisasi 1 dan 2 (Perubahan Tingkat Partikel & Variasi Musiman)
st.sidebar.header("Filter untuk Visualisasi 1 & 2")
# Filter tahun dan bulan untuk visualisasi Perubahan Tingkat Partikel dan Variasi Musiman
selected_year = st.sidebar.selectbox("Pilih Tahun", data.index.year.unique(), index=len(data.index.year.unique())-1)
selected_start_month = st.sidebar.selectbox("Pilih Bulan Awal (Range 3 Bulan)", data.index.month.unique())
end_month = (selected_start_month + 2) % 12  # Batas bulan range 3 bulan
if end_month == 0: 
    end_month = 12

# Filter data untuk 3 bulan terakhir di tahun terpilih
start_date = f"{selected_year}-{selected_start_month:02d}-01"
end_date = f"{selected_year}-{end_month:02d}-28"
filtered_data_3_months = data[start_date:end_date]

# **1. Perubahan Tingkat Partikel (PM2.5 dan PM10) dalam Tiga Bulan Terakhir**
st.subheader(f"Perubahan Tingkat Partikel (PM2.5 dan PM10) dalam Tiga Bulan Terakhir ({selected_year})")

pm_changes = filtered_data_3_months[['PM2.5', 'PM10']].resample('D').mean()

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(pm_changes.index, pm_changes['PM2.5'], label='PM2.5', color='blue')
ax.plot(pm_changes.index, pm_changes['PM10'], label='PM10', color='orange')
ax.set_title('Tingkat PM2.5 dan PM10 Selama Tiga Bulan Terakhir')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Konsentrasi (µg/m³)')
ax.legend()
ax.grid()
st.pyplot(fig)

# **Variasi Musiman antara Musim Panas dan Musim Dingin**
st.subheader(f"Variasi Musiman antara Musim Panas dan Musim Dingin ({selected_year})")
data['musim'] = np.where((data.index.month >= 6) & (data.index.month <= 8), 'Musim Panas', 'Musim Dingin')
filtered_data_year = data[data.index.year == selected_year]
seasonal_analysis = filtered_data_year.groupby('musim')[['PM2.5', 'PM10']].mean()

fig, ax = plt.subplots(figsize=(8, 6))
seasonal_analysis.plot(kind='bar', ax=ax)
ax.set_title('Rata-rata Tingkat PM2.5 dan PM10 Berdasarkan Musim')
ax.set_ylabel('Konsentrasi (µg/m³)')
ax.set_xticklabels(seasonal_analysis.index, rotation=0)
st.pyplot(fig)

# ---------------------------------------
# Filter untuk Analisa Lanjutan
st.sidebar.header("Filter untuk Analisa Lanjutan")
# Checkbox untuk menampilkan atau menyembunyikan analisa lanjutan
show_advanced_analysis = st.sidebar.checkbox("Tampilkan Analisa Lanjutan", value=True)

if show_advanced_analysis:
    # Filter tahun, bulan awal, dan jumlah hari untuk analisis lanjutan
    selected_start_year = st.sidebar.selectbox("Pilih Tahun Awal", data.index.year.unique())
    selected_start_month_analysis = st.sidebar.selectbox("Pilih Bulan Awal untuk Analisa Lanjutan", data.index.month.unique())
    selected_num_days = st.sidebar.slider("Pilih Jumlah Hari", min_value=1, max_value=365, value=30)

    # Tentukan tanggal mulai dan akhir
    start_date_analysis = pd.Timestamp(f"{selected_start_year}-{selected_start_month_analysis:02d}-01")
    end_date_analysis = start_date_analysis + pd.DateOffset(days=selected_num_days)
    filtered_data_analysis = data[start_date_analysis:end_date_analysis]

    st.subheader(f"Analisis Lanjutan Runtun Waktu Konsentrasi Polutan ({selected_start_year}-{selected_start_month_analysis:02d})")

    fig, axs = plt.subplots(6, 1, figsize=(18, 12), sharex=True)
    axs[0].plot(filtered_data_analysis.index, filtered_data_analysis['PM2.5'], label='PM2.5', color='blue')
    axs[0].set_ylabel('PM2.5 (µg/m³)')
    axs[1].plot(filtered_data_analysis.index, filtered_data_analysis['PM10'], label='PM10', color='orange')
    axs[1].set_ylabel('PM10 (µg/m³)')
    axs[2].plot(filtered_data_analysis.index, filtered_data_analysis['SO2'], label='SO2', color='green')
    axs[2].set_ylabel('SO2 (µg/m³)')
    axs[3].plot(filtered_data_analysis.index, filtered_data_analysis['NO2'], label='NO2', color='purple')
    axs[3].set_ylabel('NO2 (µg/m³)')
    axs[4].plot(filtered_data_analysis.index, filtered_data_analysis['CO'], label='CO', color='yellow')
    axs[4].set_ylabel('CO (µg/m³)')
    axs[5].plot(filtered_data_analysis.index, filtered_data_analysis['O3'], label='O3', color='red')
    axs[5].set_ylabel('O3 (µg/m³)')
    axs[5].set_xlabel('Tanggal')

    fig.suptitle(f'Runtun Waktu Konsentrasi Polutan ({selected_start_year})')
    plt.grid(True)
    st.pyplot(fig)
