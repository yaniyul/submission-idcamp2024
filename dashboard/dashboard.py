import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown(
    "<h3 style='text-align: center;'>Selamat datang di</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<h1 style='text-align: center;'>VISUALISASI KUALITAS UDARA</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<br><p style='text-align: justify;'>Aplikasi ini menampilkan visualisasi kualitas udara berdasarkan data PM2.5 yang diukur di Stasiun Dongsi.</p>",
    unsafe_allow_html=True
)

def load_data():
    file_path = "dashboard/all_data.csv"
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])  # Kombinasikan kolom waktu
    df['Tanggal'] = df['datetime'].dt.date  # Ambil hanya bagian tanggal
    return df

data = load_data()

st.sidebar.markdown(
    "<h3 style='text-align: center;'>Rentang Tanggal</h3>",
    unsafe_allow_html=True
)
start_date = st.sidebar.date_input("📅 Mulai Tanggal", value=data['Tanggal'].min())
end_date = st.sidebar.date_input("📅 Sampai Tanggal", value=data['Tanggal'].max())

filtered_data = data[(data['Tanggal'] >= start_date) & (data['Tanggal'] <= end_date)]

dongsi_daily_avg = filtered_data.groupby('Tanggal')['PM2.5'].mean()

st.write("## 📊 Grafik Rata-rata PM2.5 per Bulan")

filtered_data['Bulan'] = filtered_data['datetime'].dt.month
monthly_avg_pm25 = filtered_data.groupby('Bulan')['PM2.5'].mean()

fig2, ax2 = plt.subplots(figsize=(10, 6))
monthly_avg_pm25.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax2)

ax2.set_title('Rata-rata PM2.5 per Bulan', fontsize=14)
ax2.set_xlabel('Bulan', fontsize=12)
ax2.set_ylabel('Rata-rata PM2.5', fontsize=12)

bulan_names = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
ax2.set_xticks(range(len(bulan_names)))
ax2.set_xticklabels(bulan_names, rotation=45)

ax2.grid(axis='y', linestyle='--', alpha=0.7)

st.pyplot(fig2)

st.write(f"## 📈 Grafik Rata-rata Harian PM2.5 [{start_date} - {end_date}] di Stasiun Dongsi")

plt.figure(figsize=(14, 7))
plt.plot(dongsi_daily_avg.index, dongsi_daily_avg.values, label='Historical PM2.5', color='red', linewidth=1.5)

plt.title(f'Kualitas Udara di Stasiun Dongsi (PM2.5 per Hari) [{start_date} - {end_date}]', fontsize=14)
plt.xlabel('Tanggal', fontsize=12)
plt.ylabel('Rata-rata PM2.5', fontsize=12)
plt.axhline(75, color='green', linestyle='--', label='Batas Aman WHO (75 µg/m³)')
plt.legend()

plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)