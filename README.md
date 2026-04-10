# 📊 Datathon Dicoding — Analisis Harga Bahan Pokok Harian (2023–2025)

Dataset harga harian bahan pokok di Indonesia selama 3 tahun (2023, 2024, 2025).

## 📁 Struktur Dataset

| File | Periode | Jumlah Hari Data |
|------|---------|------------------|
| `2023.xlsx` | 02 Jan 2023 – 29 Des 2023 | 260 hari kerja |
| `2024.xlsx` | 01 Jan 2024 – 31 Des 2024 | 262 hari kerja |
| `2025.xlsx` | 01 Jan 2025 – 31 Des 2025 | 261 hari kerja |

## 🛒 Komoditas yang Dipantau (18 Komoditas)

| Kategori | Komoditas |
|----------|-----------|
| **Beras** | Bawah I, Bawah II, Medium I, Medium II, Super I, Super II |
| **Daging Ayam** | Ayam Ras Segar |
| **Daging Sapi** | Kualitas 1 |
| **Telur Ayam** | Ras Segar |
| **Bawang Merah** | Ukuran Sedang |
| **Bawang Putih** | Ukuran Sedang |
| **Cabai Merah** | Keriting |
| **Cabai Rawit** | Hijau |
| **Minyak Goreng** | Curah, Kemasan Bermerk 1, Kemasan Bermerk 2 |
| **Gula Pasir** | Kualitas Premium, Lokal |

## 📈 Highlights

- **Kenaikan tertinggi (2023→2025):** Minyak Goreng Curah (+29.54%), Daging Ayam (+29.28%)
- **Komoditas paling stabil:** Daging Sapi Kualitas 1 (~Rp 150,000, perubahan hanya -0.21%)
- **Komoditas paling volatil:** Cabai Merah Keriting (CV 35.52% di 2025, range Rp 24,000 – Rp 152,500)

## 📝 Dokumentasi

Lihat [data_analysis.md](data_analysis.md) untuk analisis lengkap data.

## ⚙️ Format Data

- Harga dalam **Rupiah (Rp)** dengan format string berkoma (contoh: `"20,000"`)
- Kolom tanggal berformat `DD/ MM/ YYYY`
- Data hanya mencakup **hari kerja** (Senin–Jumat)

## 📄 Lisensi

Dataset ini digunakan untuk keperluan Datathon Dicoding.
