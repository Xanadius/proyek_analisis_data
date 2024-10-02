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
numeric_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
for col in numeric_columns:
    # Ubah menjadi numerik, buat nilai non-numerik menjadi NaN
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Cek nilai NaN setelah konversi
print("Jumlah Nilai NaN setelah Pembersihan:")
print(data[numeric_columns].isna().sum())

# Hapus baris yang memiliki nilai NaN di kolom yang relevan
data.dropna(subset=numeric_columns, inplace=True)

# Set konfigurasi halaman
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Judul dashboard
st.title("Air Quality Analysis Dashboard")

# Sidebar untuk filter
st.sidebar.title("Filter Options")
selected_month = st.sidebar.selectbox("Select Month", data['month'].unique())
selected_hour = st.sidebar.selectbox("Select Hour", data['hour'].unique())

# Filter data berdasarkan bulan dan jam yang dipilih
filtered_data = data[(data['month'] == selected_month) & (data['hour'] == selected_hour)]

# Tren kualitas udara
st.subheader("Air Quality Trend in the Selected Month")
monthly_trend = data[data['month'] == selected_month].groupby('day').mean(numeric_only=True).reset_index()

# Cek jika monthly_trend tidak kosong
if not monthly_trend.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_trend['day'], monthly_trend['PM2.5'], label='PM2.5', color='b')
    ax.plot(monthly_trend['day'], monthly_trend['PM10'], label='PM10', color='g')
    ax.plot(monthly_trend['day'], monthly_trend['SO2'], label='SO2', color='c')
    ax.plot(monthly_trend['day'], monthly_trend['NO2'], label='NO2', color='y')
    ax.plot(monthly_trend['day'], monthly_trend['O3'], label='O3', color='r')
    ax.set_xlabel("Day of Month")
    ax.set_ylabel("Pollutant Levels")
    ax.set_title(f"Air Quality Trend for Month {selected_month}")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("No data available for the selected month.")

# Korelasi antara polutan dan waktu
st.subheader("Correlation Between Pollutants and Time of Day")
corr_matrix = data[numeric_columns].corr()  # Hanya kolom numerik

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']], annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Correlation Matrix of Pollutants")
st.pyplot(fig)

# Scatter plot polutan
st.subheader(f"Scatter Plot of Pollutants at Hour {selected_hour}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='hour', y='PM2.5', label='PM2.5', ax=ax, color='blue')
sns.scatterplot(data=filtered_data, x='hour', y='PM10', label='PM10', ax=ax, color='green')
sns.scatterplot(data=filtered_data, x='hour', y='SO2', label='SO2', ax=ax, color='cyan')
sns.scatterplot(data=filtered_data, x='hour', y='NO2', label='NO2', ax=ax, color='yellow')
sns.scatterplot(data=filtered_data, x='hour', y='O3', label='O3', ax=ax, color='red')

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Pollutant Levels")
ax.set_title(f"Pollutants vs Time of Day at Hour {selected_hour}")
ax.legend()

st.pyplot(fig)

# Footer
st.sidebar.markdown("## Air Quality Data Dashboard © 2024. Albertus Magnus Foresta Noventona")
