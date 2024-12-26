import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Visualisasi Kualitas Udara (PM2.5)")

# Penjelasan aplikasi
st.write("Aplikasi ini menampilkan visualisasi kualitas udara berdasarkan data PM2.5 yang diukur di Stasiun Dongsi.")

# Fungsi untuk memuat data
def load_data():
    # Memuat data dari file CSV
    file_path = "dashboard/all_data.csv"
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])  # Kombinasikan kolom waktu
    df['Tanggal'] = df['datetime'].dt.date  # Ambil hanya bagian tanggal
    return df

# Memuat data
data = load_data()

# Menghitung rata-rata harian dan data prediksi
# Mengelompokkan data berdasarkan tanggal untuk rata-rata harian
dongsi_daily_avg = data.groupby('Tanggal')['PM2.5'].mean()

# Membuat data prediksi untuk 7 hari ke depan
if not data.empty:
    future_dates = pd.date_range(start=data['datetime'].max() + pd.Timedelta(hours=1), periods=7, freq='D')
else:
    future_dates = pd.date_range(start=pd.Timestamp.now(), periods=7, freq='D')
future_data = pd.DataFrame({
    'datetime': future_dates,
    'PM2.5': [50 + i * 5 for i in range(7)]  # Contoh data prediksi
})

# Plot visualisasi pertama (Rata-rata per Bulan)
st.write("## Grafik Rata-rata PM2.5 per Bulan")

# Menghitung rata-rata bulanan
data['Bulan'] = data['datetime'].dt.month
monthly_avg_pm25 = data.groupby('Bulan')['PM2.5'].mean()

fig2, ax2 = plt.subplots(figsize=(10, 6))
monthly_avg_pm25.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax2)

# Atur judul dan label
ax2.set_title('Rata-rata PM2.5 per Bulan', fontsize=14)
ax2.set_xlabel('Bulan', fontsize=12)
ax2.set_ylabel('Rata-rata PM2.5', fontsize=12)

# Mengubah angka bulan menjadi nama bulan dengan rotasi 45 derajat
bulan_names = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
ax2.set_xticks(range(len(bulan_names)))
ax2.set_xticklabels(bulan_names, rotation=45)

# Menambahkan grid
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# Tampilkan plot kedua di Streamlit
st.pyplot(fig2)

# Plot visualisasi kedua
st.write("## Grafik Rata-rata Harian PM2.5")

plt.figure(figsize=(14, 7))
plt.plot(dongsi_daily_avg.index, dongsi_daily_avg.values, label='Historical PM2.5', color='red', linewidth=1.5)
plt.plot(future_data['datetime'], future_data['PM2.5'], label='Projected PM2.5 (Next 7 Days)', color='blue', linestyle='--')

# Menambahkan judul dan label
plt.title('Kualitas Udara di Stasiun Dongsi (PM2.5 per Hari)', fontsize=14)
plt.xlabel('Tanggal', fontsize=12)
plt.ylabel('Rata-rata PM2.5', fontsize=12)
plt.axhline(75, color='green', linestyle='--', label='Batas Aman WHO (75 µg/m³)')
plt.legend()

# Menambahkan grid dan menampilkan plot
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)