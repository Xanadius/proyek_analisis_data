import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("dashboard/PRSA_Data_Aotizhongxin_20130301-20170228.csv")

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

st.title("Air Quality Analysis Dashboard")

st.sidebar.title("Filter Options")

selected_month = st.sidebar.selectbox("Select Month", data['month'].unique())

selected_hour = st.sidebar.selectbox("Select Hour", data['hour'].unique())

filtered_data = data[(data['month'] == selected_month) & (data['hour'] == selected_hour)]

st.subheader("Air Quality Trend in the Selected Month")

monthly_trend = data[data['month'] == selected_month].groupby('day').mean()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_trend.index, monthly_trend['PM2.5'], label='PM2.5', color='b')
ax.plot(monthly_trend.index, monthly_trend['PM10'], label='PM10', color='g')
ax.plot(monthly_trend.index, monthly_trend['O3'], label='O3', color='r')
ax.set_xlabel("Day of Month")
ax.set_ylabel("Pollutant Levels")
ax.set_title(f"Air Quality Trend for Month {selected_month}")
ax.legend()

st.pyplot(fig)

st.subheader("Correlation Between Pollutants and Time of Day")

corr_matrix = data.corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']], annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Correlation Matrix of Pollutants")
st.pyplot(fig)

st.subheader(f"Scatter Plot of Pollutants at Hour {selected_hour}")

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='hour', y='PM2.5', label='PM2.5', ax=ax, color='blue')
sns.scatterplot(data=filtered_data, x='hour', y='PM10', label='PM10', ax=ax, color='green')
sns.scatterplot(data=filtered_data, x='hour', y='O3', label='O3', ax=ax, color='red')

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Pollutant Levels")
ax.set_title(f"Pollutants vs Time of Day at Hour {selected_hour}")
ax.legend()

st.pyplot(fig)

st.sidebar.markdown("## Air Quality Data Dashboard © 2024. Albertus Magnus Foresta Noventona")
