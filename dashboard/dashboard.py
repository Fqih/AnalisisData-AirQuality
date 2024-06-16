import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Air Quality Analysis")

# Load data from GitHub repository
data = pd.read_csv('https://raw.githubusercontent.com/Fqih/AnalisisData/main/dashboard/all_data.csv')
data['date'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])

st.sidebar.title('Filters')
st.sidebar.subheader('Date Range Selection')

minDate = data['date'].min()
maxDate = data['date'].max()

defaultStartDate = pd.Timestamp('2015-02-20')
defaultEndDate = pd.Timestamp('2015-10-20')

startDate, endDate = st.sidebar.date_input(
    label='Select Date Range',
    min_value=minDate.date(),
    max_value=maxDate.date(),
    value=(defaultStartDate.date(), defaultEndDate.date())
)

filteredData = data[(data['date'] >= pd.to_datetime(startDate)) & (data['date'] <= pd.to_datetime(endDate))]

def createDailyPm25Df(df):
    dailyPm25Df = df.resample(rule='D', on='date')['PM2.5'].mean().reset_index()
    return dailyPm25Df

def createSeasonalPm10Df(df):
    seasonalPm10Df = df.groupby('season')['PM10'].mean().reset_index()
    return seasonalPm10Df

dailyPm25Df = createDailyPm25Df(filteredData)
seasonalPm10Df = createSeasonalPm10Df(filteredData)

st.title('Air Quality Analysis Dashboard')
st.subheader('Data Diri')
st.markdown(
    """
    Nama    : Muhammad Faqih Hakim

    Email   : mhmdfkih21@gmail.com
    """
)

st.write(data)

st.header('Kadar PM2.5')

avgPm25 = round(dailyPm25Df['PM2.5'].mean(), 2)
st.metric("Average PM2.5", value=avgPm25)
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='date', y='PM2.5', data=dailyPm25Df, color='blue')
ax.set_title('Daily PM2.5 Levels Trend')
ax.set_xlabel('Date')
ax.set_ylabel('PM2.5')
ax.xaxis.set_major_locator(plt.MaxNLocator(6))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.header('Kadar PM10 Setiap Musim')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='PM10', data=seasonalPm10Df, palette='viridis')
ax.set_title('Seasonal Average PM10 Levels')
ax.set_xlabel('Season')
ax.set_ylabel('PM10')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

numericColumns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO/10', 'O3']

st.header('Kadar Polutan Berdasarkan Bulan')
fig, ax = plt.subplots(figsize=(10, 6))
monthlyAvg = filteredData.groupby('month')[numericColumns].mean().reset_index()
sns.lineplot(data=monthlyAvg.set_index('month'))
plt.title('Rata-rata Kadar Polutan Berdasarkan Bulan')
plt.xlabel('Bulan')
plt.ylabel('Kadar Polutan')
plt.legend(labels=numericColumns)
plt.grid(True)
st.pyplot(fig)

st.header('Kadar Polutan Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10, 6))
seasonalAvg = filteredData.groupby('season')[numericColumns].mean().reset_index()
seasonalAvg = seasonalAvg.melt(id_vars='season', var_name='Pollutant', value_name='Concentration')
sns.barplot(x='season', y='Concentration', hue='Pollutant', data=seasonalAvg)
plt.title('Rata-rata Kadar Polutan Berdasarkan Musim Tertentu')
plt.xlabel('Musim')
plt.ylabel('Kadar Polutan')
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.header('Hubungan Curah Hujan dengan Polusi')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='RAIN', y='PM2.5', data=filteredData, label='PM2.5')
sns.scatterplot(x='RAIN', y='PM10', data=filteredData, label='PM10')
sns.scatterplot(x='RAIN', y='SO2', data=filteredData, label='SO2')
sns.scatterplot(x='RAIN', y='NO2', data=filteredData, label='NO2')
sns.scatterplot(x='RAIN', y='CO/10', data=filteredData, label='CO')
plt.title('Hubungan Curah Hujan dengan Konsentrasi Polutan')
plt.xlabel('Curah Hujan')
plt.ylabel('Konsentrasi')
plt.legend()
st.pyplot(fig)

st.header('Kadar Polusi Dalam Sehari')
fig, ax = plt.subplots(figsize=(10, 6))
hourlyAvg = filteredData.groupby('hour')[numericColumns].mean().reset_index()
sns.lineplot(x='hour', y='PM2.5', data=hourlyAvg, label='PM2.5', color='red')
sns.lineplot(x='hour', y='PM10', data=hourlyAvg, label='PM10', color='blue')
sns.lineplot(x='hour', y='SO2', data=hourlyAvg, label='SO2', color='orange')
sns.lineplot(x='hour', y='NO2', data=hourlyAvg, label='NO2', color='green')
sns.lineplot(x='hour', y='CO/10', data=hourlyAvg, label='CO', color='yellow')
sns.lineplot(x='hour', y='O3', data=hourlyAvg, label='O3', color='black')
plt.title('Rata-rata Kadar Polutan Berdasarkan Jam dalam Sehari')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Kadar Polutan')
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.header('Tren Bulanan')
fig, ax = plt.subplots(figsize=(10, 6))
filteredData.set_index('date')[numericColumns].resample('M').mean().plot(ax=ax)
plt.title('Tren Bulanan Polutan Udara')
plt.xlabel('Bulan')
plt.ylabel('Konsentrasi')
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.caption('Copyright © Faqih 2024')
