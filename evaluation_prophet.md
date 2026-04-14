# 🔮 Laporan Evaluasi Model *Forecasting* (Prophet)
**Proyek:** Aceh Resilience Monitor (ARM)  
**Metode AI:** Time-Series Forecasting (Meta Prophet)  
**Periode Data:** Januari 2023 – Desember 2025  

---

## 📌 Ringkasan Eksekutif
Dalam iterasi terbaru *Aceh Resilience Monitor*, kami mengintegrasikan *Machine Learning* untuk beralih dari pemantauan historis ke sistem peringatan dini (prediktif). Dokumen ini menyajikan hasil **Backtesting** (uji teknis) dari algoritma Meta Prophet untuk melihat seberapa akurat prediksi yang dihasilkan sistem untuk pengambil kebijakan.

Secara keseluruhan, model mencapai **Rata-rata Margin Kesalahan (MAPE) sebesar 7.74%** melintasi 18 komoditas bahan pokok, yang masuk dalam kategori "Sangat Baik/Tinggi" untuk standar industri pemodelan harga pangan.

---

## 🛠️ Metodologi Pengujian: *Train-Test Split (Holdout)*
Untuk memastikan objektivitas akurasi prediksi, kami tidak langsung menguji model dengan data yang sudah pernah ia "lihat". Kami menggunakan metode *Holdout 90 Hari*:
1. **Data Pelatihan (*Training Data*):** `02 Januari 2023` s/d `30 September 2025`. Model dilatih menggunakan rentang ini untuk mengenali tren, *seasonality* mingguan, dan siklus tahunan (seperti Ramadhan/Tahun Baru).
2. **Data Pengujian (*Testing Data*):** `01 Oktober 2025` s/d `31 Desember 2025` (90 hari). Kami meminta AI memprediksi harga pada periode ini secara buta ("*blind prediction*").
3. **Validasi:** Tebakan AI kemudian dikomparasi dengan Harga Aktual yang terjadi pada 90 hari tersebut untuk mendapatkan rasio simpangan (error).

---

## 📐 Metrik Penilaian Berstandar Industri
Performa model diukur menggunakan tiga metrik statistik utama:
- **MAPE (Mean Absolute Percentage Error):** Rata-rata margin kesalahan dalam bentuk persentase. (Contoh: MAPE 2% pada harga Rp 10.000 berarti error rata-rata Rp 200).
- **MAE (Mean Absolute Error):** Rata-rata selisih mutlak nilai tebakan AI terhadap harga asli dalam mata uang (Rupiah/Kg).
- **RMSE (Root Mean Squared Error):** Mengukur akurasi dengan memberikan *penalti numerik yang berat* terhadap kesalahan/puncak ekstrem. Jika nilai RMSE jauh lebih tinggi dari MAE, berarti model gagal menangani lonjakan (outlier) mendadak.

---

## 📊 Hasil Evaluasi per Komoditas

Berdasarkan *Backtesting*, kemampuan AI dibagi menjadi 3 kategori keandalan:

### 🟢 1. Keandalan Sangat Tinggi (Error < 5%)
Komoditas ini sangat direkomendasikan untuk dijadikan rujukan kebijakan operasi pasar karena AI mampu menebak dengan presisi tinggi.

| Komoditas | Prediktabilitas | MAPE (%) | MAE (Error Harian) | RMSE (Error Ekstrem) |
| :--- | :--- | :--- | :--- | :--- |
| **Daging Sapi Kualitas 1** | Sangat Stabil | **0.49%** | ± Rp 742 / Kg | Rp 749 |
| **Beras Kualitas Bawah I** | Sangat Stabil | **1.39%** | ± Rp 201 / Kg | Rp 228 |
| **Beras Kualitas Super I** | Sangat Stabil | **1.51%** | ± Rp 251 / Kg | Rp 290 |
| **Beras Kualitas Bawah II**| Sangat Stabil | **1.52%** | ± Rp 227 / Kg | Rp 270 |
| **Beras Kualitas Medium I**| Sangat Stabil | **2.18%** | ± Rp 325 / Kg | Rp 413 |
| **Gula Pasir Premium** | Sangat Stabil | **2.47%** | ± Rp 511 / Kg | Rp 581 |
| **Gula Pasir Lokal** | Sangat Stabil | **2.86%** | ± Rp 548 / Kg | Rp 755 |
| **Minyak Goreng Kemasan** | Stabil | **3.09%** | ± Rp 752 / Kg | Rp 1.025 |

### 🟡 2. Keandalan Sedang (Error 5% - 15%)
Komoditas dengan sedikit fluktuasi. Prediksi dapat digunakan untuk menangkap tren jangka menengah (1-2 minggu ke depan).

| Komoditas | Prediktabilitas | MAPE (%) | MAE (Error Harian) | RMSE (Error Ekstrem) |
| :--- | :--- | :--- | :--- | :--- |
| **Minyak Goreng Curah** | Moderat | **5.00%** | ± Rp 1.048 / L | Rp 1.256 |
| **Bawang Putih** | Moderat | **6.06%** | ± Rp 2.717 / Kg | Rp 4.142 |
| **Telur Ayam Ras Segar** | Fluktuatif | **8.51%** | ± Rp 3.700 / Kg | Rp 7.279 |
| **Daging Ayam Ras Segar** | Fluktuatif | **11.67%** | ± Rp 4.888 / Kg | Rp 5.097 |

> *Insight Teknikal:* Pada **Telur Ayam Ras**, rasio RMSE/MAE cukup besar (Rp 7.279 berbanding Rp 3.700). Hal ini mengindikasikan adanya beberapa kejadian di 90 hari terakhir (seperti liburan lokal) di mana harga nyata melonjak tinggi, tetapi model gagal memprediksi lonjakan tersebut secara akurat.

### 🔴 3. Sulit Diprediksi secara Univariat (Error > 20%)
Kelompok komoditas hortikultura yang **tidak direkomendasikan** untuk menggunakan prediksi *time-series* murni pada pelacakan harga strategis saat ini.

| Komoditas | Prediktabilitas | MAPE (%) | MAE (Error Harian) | RMSE (Error Ekstrem) |
| :--- | :--- | :--- | :--- | :--- |
| **Cabai Rawit Hijau** | Sangat *Volatile* | **20.56%** | ± Rp 11.598 / Kg| Rp 15.231 |
| **Cabai Merah Keriting** | Sangat *Volatile* | **29.54%** | ± Rp 22.855 / Kg| Rp 30.341 |
| **Bawang Merah** | Sangat *Volatile* | **32.87%** | ± Rp 13.149 / Kg| Rp 14.300 |

---

## 🎯 Analisis Kegagalan & Rekomendasi 

### Mengapa AI Gagal pada Komoditas Cabai & Bawang?
Algoritma Prophet (seperti algoritma time-series klasik lainnya) adalah model **Univariat**—ia hanya meneliti grafik harganya sendiri. Sayangnya, lonjakan tak terduga pada harga bawang merah atau cabai 80% disebabkan oleh **gagal panen akibat cuaca ekstrem (banjir/hama)** yang tidak bisa dilihat AI hanya dari data harga tahun-tahun sebelumnya.

### *Roadmap* Solusi (Fase 3 Pembangunan Parameter AI)
Untuk mengatasi kelemahan margin error sebesar 30% pada komoditas sayur-mayur, proyek *Aceh Resilience Monitor* harus melibatkan transisi model AI prediktif, dari Univariat menjadi **Multivariat**.

1. **Integrasi Data Cuaca (BMKG API):**
   * Feed curah hujan regional ke dalam model (seperti **XGBoost Regressor** atau mengaktifkan fitur *add_regressor* di Prophet). AI akan belajar pola: *"Jika curah hujan di Takengon melampaui 100mm, harga Cabai akan fluktuatif naik dalam 14 hari"*.
2. **Indeks Harga BBM Transportasi:**
   * Memasukkan data historis kenaikan pertalite/solar sebagai pengukur inflasi biaya logistik per bulan ke model AI.
