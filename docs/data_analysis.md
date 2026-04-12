# 📊 Analisis Data Harga Bahan Pokok Harian (2023–2025)

## 1. Deskripsi Dataset

Dataset ini berisi **harga harian bahan pokok** di Indonesia selama 3 tahun (2023, 2024, 2025), disimpan dalam 3 file Excel terpisah.

> [!NOTE]
> Data hanya mencakup **hari kerja** (Senin–Jumat), tidak termasuk akhir pekan dan hari libur nasional.

### Ringkasan File

| File | Sheet | Baris (Komoditas) | Kolom Tanggal | Periode |
|------|-------|-------------------|---------------|---------|
| `2023.xlsx` | Sheet | 28 (18 komoditas + 10 header) | 260 | 02 Jan 2023 – 29 Des 2023 |
| `2024.xlsx` | Sheet | 28 (18 komoditas + 10 header) | 262 | 01 Jan 2024 – 31 Des 2024 |
| `2025.xlsx` | Sheet | 28 (18 komoditas + 10 header) | 261 | 01 Jan 2025 – 31 Des 2025 |

### Struktur Data

Setiap file memiliki struktur yang sama:

- **Kolom 1**: `No` — Nomor urut komoditas atau penomoran kategori (I, II, III, dst.)
- **Kolom 2**: `Komoditas (Rp)` — Nama komoditas / header kategori
- **Kolom 3–N**: Tanggal harian (format `DD/ MM/ YYYY`) — Harga dalam Rupiah (Rp)

> [!IMPORTANT]
> Semua data bertipe `object` (string), bukan numerik. Nilai harga menggunakan format ribuan dengan koma (contoh: `20,000`). Konversi diperlukan sebelum analisis numerik.

---

## 2. Daftar Komoditas

Dataset mencakup **10 kategori** dengan total **18 komoditas**:

| No | Kategori | Komoditas |
|----|----------|-----------|
| I | Beras | 1. Beras Kualitas Bawah I |
| | | 2. Beras Kualitas Bawah II |
| | | 3. Beras Kualitas Medium I |
| | | 4. Beras Kualitas Medium II |
| | | 5. Beras Kualitas Super I |
| | | 6. Beras Kualitas Super II |
| II | Daging Ayam | 1. Daging Ayam Ras Segar |
| III | Daging Sapi | 1. Daging Sapi Kualitas 1 |
| IV | Telur Ayam | 1. Telur Ayam Ras Segar |
| V | Bawang Merah | 1. Bawang Merah Ukuran Sedang |
| VI | Bawang Putih | 1. Bawang Putih Ukuran Sedang |
| VII | Cabai Merah | 1. Cabai Merah Keriting |
| VIII | Cabai Rawit | 1. Cabai Rawit Hijau |
| IX | Minyak Goreng | 1. Minyak Goreng Curah |
| | | 2. Minyak Goreng Kemasan Bermerk 1 |
| | | 3. Minyak Goreng Kemasan Bermerk 2 |
| X | Gula Pasir | 1. Gula Pasir Kualitas Premium |
| | | 2. Gula Pasir Lokal |

---

## 3. Statistik Deskriptif per Tahun

### 3.1 Tahun 2023

| Komoditas | Min (Rp) | Max (Rp) | Mean (Rp) | Std Dev |
|-----------|----------|----------|-----------|---------|
| Beras Kualitas Bawah I | 10,900 | 13,250 | 11,782 | 832 |
| Beras Kualitas Bawah II | 11,200 | 13,700 | 12,190 | 827 |
| Beras Kualitas Medium I | 11,450 | 13,400 | 12,235 | 699 |
| Beras Kualitas Medium II | 11,350 | 13,350 | 12,164 | 675 |
| Beras Kualitas Super I | 12,950 | 15,000 | 13,822 | 710 |
| Beras Kualitas Super II | 12,100 | 14,200 | 12,970 | 749 |
| Daging Ayam Ras Segar | 24,500 | 35,000 | 29,573 | 2,694 |
| Daging Sapi Kualitas 1 | 150,000 | 180,000 | 150,912 | 4,051 |
| Telur Ayam Ras Segar | 25,100 | 32,150 | 28,270 | 1,741 |
| Bawang Merah Ukuran Sedang | 25,250 | 45,000 | 35,877 | 5,249 |
| Bawang Putih Ukuran Sedang | 26,750 | 47,800 | 36,385 | 5,318 |
| Cabai Merah Keriting | 24,250 | 68,750 | 42,447 | 11,005 |
| Cabai Rawit Hijau | 30,000 | 68,250 | 44,356 | 10,061 |
| Minyak Goreng Curah | 14,750 | 16,000 | 15,398 | 272 |
| Minyak Goreng Kemasan Bermerk 1 | 21,500 | 23,250 | 21,993 | 418 |
| Minyak Goreng Kemasan Bermerk 2 | 20,250 | 22,250 | 21,069 | 537 |
| Gula Pasir Kualitas Premium | 16,150 | 17,750 | 16,943 | 509 |
| Gula Pasir Lokal | 15,000 | 17,750 | 15,519 | 877 |

> Data valid: 255 dari 260 titik data per komoditas (5 missing values, kemungkinan hari libur).

---

### 3.2 Tahun 2024

| Komoditas | Min (Rp) | Max (Rp) | Mean (Rp) | Std Dev |
|-----------|----------|----------|-----------|---------|
| Beras Kualitas Bawah I | 13,100 | 13,700 | 13,340 | 146 |
| Beras Kualitas Bawah II | 13,250 | 13,900 | 13,580 | 183 |
| Beras Kualitas Medium I | 13,050 | 14,100 | 13,823 | 166 |
| Beras Kualitas Medium II | 13,250 | 14,000 | 13,852 | 110 |
| Beras Kualitas Super I | 14,500 | 15,600 | 15,301 | 169 |
| Beras Kualitas Super II | 14,000 | 14,600 | 14,377 | 100 |
| Daging Ayam Ras Segar | 27,750 | 42,000 | 34,212 | 3,667 |
| Daging Sapi Kualitas 1 | 150,000 | 160,000 | 150,172 | 1,103 |
| Telur Ayam Ras Segar | 26,800 | 32,850 | 28,925 | 1,414 |
| Bawang Merah Ukuran Sedang | 27,250 | 68,250 | 41,100 | 10,220 |
| Bawang Putih Ukuran Sedang | 38,750 | 45,750 | 41,933 | 1,820 |
| Cabai Merah Keriting | 26,500 | 90,000 | 44,851 | 14,149 |
| Cabai Rawit Hijau | 38,750 | 77,500 | 50,722 | 6,983 |
| Minyak Goreng Curah | 15,250 | 21,000 | 17,991 | 1,469 |
| Minyak Goreng Kemasan Bermerk 1 | 21,250 | 22,250 | 21,717 | 304 |
| Minyak Goreng Kemasan Bermerk 2 | 20,000 | 22,250 | 20,771 | 545 |
| Gula Pasir Kualitas Premium | 17,500 | 20,500 | 19,871 | 694 |
| Gula Pasir Lokal | 17,500 | 19,000 | 18,268 | 351 |

> Data valid: 262 dari 262 titik data per komoditas (100% lengkap).

---

### 3.3 Tahun 2025

| Komoditas | Min (Rp) | Max (Rp) | Mean (Rp) | Std Dev |
|-----------|----------|----------|-----------|---------|
| Beras Kualitas Bawah I | 12,750 | 14,950 | 13,859 | 671 |
| Beras Kualitas Bawah II | 13,800 | 15,600 | 14,565 | 688 |
| Beras Kualitas Medium I | 13,800 | 15,850 | 14,480 | 652 |
| Beras Kualitas Medium II | 13,750 | 15,500 | 14,458 | 679 |
| Beras Kualitas Super I | 15,450 | 17,300 | 16,093 | 603 |
| Beras Kualitas Super II | 14,350 | 16,350 | 15,109 | 684 |
| Daging Ayam Ras Segar | 31,750 | 45,000 | 38,232 | 2,891 |
| Daging Sapi Kualitas 1 | 150,000 | 175,000 | 150,594 | 3,242 |
| Telur Ayam Ras Segar | 25,650 | 60,200 | 30,246 | 4,554 |
| Bawang Merah Ukuran Sedang | 35,000 | 65,000 | 44,436 | 7,019 |
| Bawang Putih Ukuran Sedang | 37,500 | 49,000 | 42,984 | 3,147 |
| Cabai Merah Keriting | 24,000 | 152,500 | 53,019 | 18,835 |
| Cabai Rawit Hijau | 33,750 | 96,250 | 49,246 | 10,818 |
| Minyak Goreng Curah | 19,250 | 22,750 | 19,946 | 833 |
| Minyak Goreng Kemasan Bermerk 1 | 22,250 | 25,500 | 22,862 | 670 |
| Minyak Goreng Kemasan Bermerk 2 | 22,250 | 25,500 | 23,057 | 642 |
| Gula Pasir Kualitas Premium | 19,500 | 20,750 | 20,530 | 296 |
| Gula Pasir Lokal | 17,850 | 19,750 | 18,744 | 342 |

> Data valid: 261 dari 261 titik data per komoditas (100% lengkap).

---

## 4. Perubahan Harga Year-over-Year (Rata-rata)

| Komoditas | 2023→2024 | 2024→2025 | 2023→2025 (Total) |
|-----------|-----------|-----------|-------------------|
| Beras Kualitas Bawah I | +13.23% | +3.89% | **+17.63%** |
| Beras Kualitas Bawah II | +11.40% | +7.25% | **+19.48%** |
| Beras Kualitas Medium I | +12.97% | +4.75% | **+18.34%** |
| Beras Kualitas Medium II | +13.88% | +4.37% | **+18.86%** |
| Beras Kualitas Super I | +10.70% | +5.17% | **+16.43%** |
| Beras Kualitas Super II | +10.85% | +5.09% | **+16.49%** |
| Daging Ayam Ras Segar | +15.69% | +11.75% | **+29.28%** 🔴 |
| Daging Sapi Kualitas 1 | -0.49% | +0.28% | **-0.21%** 🟢 |
| Telur Ayam Ras Segar | +2.32% | +4.57% | **+6.99%** |
| Bawang Merah Ukuran Sedang | +14.56% | +8.12% | **+23.86%** 🔴 |
| Bawang Putih Ukuran Sedang | +15.25% | +2.51% | **+18.14%** |
| Cabai Merah Keriting | +5.66% | +18.21% | **+24.91%** 🔴 |
| Cabai Rawit Hijau | +14.35% | -2.91% | **+11.02%** |
| Minyak Goreng Curah | +16.84% | +10.87% | **+29.54%** 🔴 |
| Minyak Goreng Kemasan Bermerk 1 | -1.26% | +5.27% | **+3.95%** |
| Minyak Goreng Kemasan Bermerk 2 | -1.42% | +11.01% | **+9.44%** |
| Gula Pasir Kualitas Premium | +17.28% | +3.31% | **+21.17%** 🔴 |
| Gula Pasir Lokal | +17.72% | +2.60% | **+20.78%** 🔴 |

> [!WARNING]
> 🔴 Komoditas dengan kenaikan total > 20% dalam 3 tahun: Daging Ayam (+29.28%), Bawang Merah (+23.86%), Cabai Merah (+24.91%), Minyak Goreng Curah (+29.54%), Gula Pasir Premium (+21.17%), Gula Pasir Lokal (+20.78%)

---

## 5. Analisis Volatilitas (Coefficient of Variation)

Coefficient of Variation (CV) mengukur tingkat fluktuasi harga relatif terhadap rata-rata. Semakin tinggi CV, semakin volatil/fluktuatif harganya.

### Top 5 Komoditas Paling Volatil per Tahun

| Peringkat | 2023 | CV | 2024 | CV | 2025 | CV |
|-----------|------|----|------|----|------|----|
| 1 | Cabai Merah Keriting | 25.93% | Cabai Merah Keriting | 31.55% | Cabai Merah Keriting | 35.52% |
| 2 | Cabai Rawit Hijau | 22.68% | Bawang Merah | 24.87% | Cabai Rawit Hijau | 21.97% |
| 3 | Bawang Merah | 14.63% | Cabai Rawit Hijau | 13.77% | Bawang Merah | 15.80% |
| 4 | Bawang Putih | 14.62% | Daging Ayam | 10.72% | Telur Ayam | 15.06% |
| 5 | Daging Ayam | 9.11% | Minyak Goreng Curah | 8.17% | Daging Ayam | 7.56% |

> [!CAUTION]
> **Cabai Merah Keriting** konsisten menjadi komoditas **paling volatil** selama 3 tahun berturut-turut, dengan CV yang terus meningkat (25.93% → 31.55% → 35.52%). Pada 2025, harga cabai merah berkisar antara Rp 24,000 hingga Rp 152,500 — selisih lebih dari **6x lipat**!

---

## 6. Insight Utama

### 📈 Tren Inflasi Bahan Pokok
- Hampir **semua komoditas** mengalami kenaikan harga dalam 3 tahun (2023–2025)
- Hanya **Daging Sapi** yang relatif stabil (~Rp 150,000) dengan perubahan minimal (-0.21%)
- **Kenaikan terbesar**: Minyak Goreng Curah (+29.54%) dan Daging Ayam (+29.28%)

### 🌶️ Komoditas Paling Fluktuatif
- **Cabai Merah Keriting** dan **Cabai Rawit Hijau** — harga berfluktuasi sangat tinggi, dipengaruhi musim panen dan cuaca
- **Bawang Merah** juga menunjukkan volatilitas tinggi

### 🔒 Komoditas Paling Stabil
- **Daging Sapi Kualitas 1** — hampir konstan di ~Rp 150,000
- **Minyak Goreng Kemasan Bermerk** — fluktuasi sangat rendah
- **Gula Pasir** — relatif stabil meski ada kenaikan bertahap

### 📊 Kualitas Data
- **2023**: 255 dari 260 data poin valid (5 missing values)
- **2024**: 262 dari 262 data poin valid (100% lengkap)
- **2025**: 261 dari 261 data poin valid (100% lengkap)
- Seluruh data bertipe string dengan format ribuan berkoma, perlu dikonversi ke numerik untuk analisis

### ⚙️ Catatan Teknis untuk Pengolahan Data
1. Kolom tanggal berformat `DD/ MM/ YYYY` (dengan spasi sebelum bulan dan tahun)
2. Baris berisi **campuran** header kategori (No = I, II, dst.) dan data komoditas (No = 1, 2, dst.)
3. Harga dalam format string dengan koma sebagai pemisah ribuan (contoh: `"20,000"`)
4. Data hanya tersedia untuk hari kerja (weekdays), sekitar 260-262 hari per tahun

---

*Dokumen ini dibuat secara otomatis dari analisis file `2023.xlsx`, `2024.xlsx`, dan `2025.xlsx`.*  
*Tanggal analisis: 10 April 2026*
