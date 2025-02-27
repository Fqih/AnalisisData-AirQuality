import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.preprocessing import RobustScaler

model_path = "Model/best_xgboost_model.pkl"
scaler_path = "Scaler/robust_scaler.pkl"
# Muat Model dan Scaler
best_model = joblib.load(model_path)
scaler_Robust = joblib.load(scaler_path)

st.set_page_config(page_title="Air Pollution & Ozone Analysis Dashboard")model_path = "Model/best_xgboost_model.pkl"
scaler_path = "Scaler/robust_scaler.pkl"
# Muat Model dan Scaler
best_model = joblib.load(model_path)
scaler_Robust = joblib.load(scaler_path)

st.set_page_config(page_title="Air Pollution & Ozone Analysis Dashboard")
best_model = joblib.load(model_path)
scaler_Robust = joblib.load(scaler_path)

st.set_page_config(page_title="Air Pollution & Ozone Analysis Dashboard")

# Load data dari GitHub repository
data = pd.read_csv('https://raw.githubusercontent.com/Fqih/AnalisisData-AirQuality/refs/heads/main/data/final_df.csv')
data['date'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])

# Sidebar untuk filter
st.sidebar.title('Filters')
st.sidebar.subheader('Date Range Selection')

minDate = data['date'].min()
maxDate = data['date'].max()

defaultStartDate = pd.Timestamp('2015-02-20')
defaultEndDate = pd.Timestamp('2016-03-20')

startDate, endDate = st.sidebar.date_input(
    label='Select Date Range',
    min_value=minDate.date(),
    max_value=maxDate.date(),
    value=(defaultStartDate.date(), defaultEndDate.date())
)

filteredData = data[(data['date'] >= pd.to_datetime(startDate)) & (data['date'] <= pd.to_datetime(endDate))]

# Fitur yang digunakan dalam model
f = ["PM2.5", "PM10", "NO2", "SO2", "CO", "PM2.5_NO2", "PM10_SO2", "CO_ratio"]

# **Prediksi Kadar O3 menggunakan Model**
scaled_features = scaler_Robust.transform(filteredData[f])
predicted_O3 = best_model.predict(scaled_features)


# Skalakan fitur sebelum prediksi
scaled_features = scaler_Robust.transform(filteredData[f])
predicted_O3 = best_model.predict(scaled_features)

# Tambahkan hasil prediksi ke dataframe
filteredData["Predicted O3"] = predicted_O3

# Fungsi untuk membuat dataframe tren harian
def createDailyPm25Df(df):
    dailyPm25Df = df.resample(rule='D', on='date')['PM2.5'].mean().reset_index()
    return dailyPm25Df

# Fungsi untuk membuat dataframe musiman
def createSeasonalPm10Df(df):
    seasonalPm10Df = df.groupby('season')['PM10'].mean().reset_index()
    return seasonalPm10Df

dailyPm25Df = createDailyPm25Df(filteredData)
seasonalPm10Df = createSeasonalPm10Df(filteredData)

st.title('Air Pollution & Ozone Monitoring')
st.subheader('Data Diri')
st.markdown(
    """
    Nama    : Muhammad Faqih Hakim

    Email   : mhmdfkih21@gmail.com
    """
)

st.write(data)

# Prediksi kadar O3
predicted_O3 = best_model.predict(scaled_features)
filteredData["Predicted O3"] = predicted_O3

st.markdown(
    """
    ### Objective
    This dashboard analyzes the impact of air pollution (PM2.5, PM10, NO2, SO2, and CO) on O3 (ozone) levels
    to better understand air pollution patterns and factors influencing ozone concentration.
    """
)

# **Visualisasi Hubungan Polutan dengan O3**
st.header("Correlation Between Pollutants and Ozone")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(filteredData[f + ["Predicted O3"]].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Matrix")
st.pyplot(fig)


# **Trend Prediksi O3**
st.header('Ozone (O3) Levels Over Time')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='date', y='Predicted O3', data=filteredData, color='purple')
plt.xlabel('Date')
plt.ylabel('Predicted O3')
plt.title('Predicted Ozone Levels Trend')
st.pyplot(fig)

st.header('Kadar PM10 Per Musim')
fig, ax = plt.subplots(figsize=(10, 6))
filteredData['PM10'] = filteredData['PM10'].clip(lower=0)  # Batasi nilai minimum ke 0
seasonalPm10Df = filteredData.groupby('season')['PM10'].mean().reset_index()
sns.barplot(x='season', y='PM10', data=seasonalPm10Df, palette='viridis')
ax.set_title('Seasonal Average PM10 Levels')
ax.set_xlabel('Season')
ax.set_ylabel('PM10')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

polutan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO']

st.header('Kadar Polutan Berdasarkan Bulan')
fig, ax = plt.subplots(figsize=(10, 6))
monthlyAvg = filteredData.groupby('month')[polutan].mean().reset_index()
sns.lineplot(data=monthlyAvg.set_index('month'))
plt.title('Rata-rata Kadar Polutan Berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Kadar Polutan')
plt.legend(labels=polutan)
plt.grid(True)
st.pyplot(fig)

st.header('Kadar Polutan Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10, 6))
seasonalAvg = filteredData.groupby('season')[f].mean().reset_index()
seasonalAvg = seasonalAvg.melt(id_vars='season', var_name='Pollutant', value_name='Concentration')
seasonalAvg['Concentration'] = seasonalAvg['Concentration'].clip(lower=0)  
sns.barplot(x='season', y='Concentration', hue='Pollutant', data=seasonalAvg)
plt.title('Rata-rata Kadar Polutan Berdasarkan Musim Tertentu')
plt.xlabel('Musim')
plt.ylabel('Kadar Polutan')
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.header('Kadar Polusi Dalam Sehari')
fig, ax = plt.subplots(figsize=(10, 6))
hourlyAvg = filteredData.groupby('hour')[polutan].mean().reset_index()
sns.lineplot(x='hour', y='PM2.5', data=hourlyAvg, label='PM2.5', color='red')
sns.lineplot(x='hour', y='PM10', data=hourlyAvg, label='PM10', color='blue')
sns.lineplot(x='hour', y='SO2', data=hourlyAvg, label='SO2', color='orange')
sns.lineplot(x='hour', y='NO2', data=hourlyAvg, label='NO2', color='green')
sns.lineplot(x='hour', y='CO', data=hourlyAvg, label='CO', color='yellow')
plt.title('Rata-rata Kadar Polutan Berdasarkan Jam dalam Sehari')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Kadar Polutan')
plt.legend()
plt.grid(True)
st.pyplot(fig)


st.caption('Copyright © Faqih 2024')
