# Project Brief: Datathon Dicoding

### Informasi Peserta
| No | Nama | Email Dicoding | Peran Utama |
|---|---|---|---|
| 1 | Aulia Muzhaffar | auliamuzhaffar@gmail.com | Machine Learning & Analytics (Forecasting Prophet, Evaluasi Model, EWS Logic) |
| 2 | Muhammad Ilhaam Ghiffari | *(Menunggu konfirmasi)* | Data Engineering & Frontend (Data Pipeline ETL, Dashboard UI/UX, Z-Score Anomaly) |
| 3 | Arief Hidayah | ariefhidayahm@gmail.com | Data Acquisition & Repo Manager (Scraping Data, GitHub Repository Management) |

**Topik:** Ketahanan Pangan & Agrikultur Modern

---

### Ringkasan Eksekutif
Volatilitas harga pangan strategis sering kali memicu lonjakan inflasi daerah. Dalam praktiknya, pengambilan keputusan oleh pemangku kebijakan sering terhambat oleh lambatnya integrasi data dan ketidakmampuan untuk memprediksi tren harga di masa depan berdasarkan data historis.

**Problem Statement:** Bagaimana menyatukan aliran data historis harga 18 komoditas pangan strategis untuk mendeteksi anomali secara *real-time* dan memprediksi lonjakan harga di masa depan guna memberikan rekomendasi intervensi pasar yang proaktif?

**Research Questions:** 
1. Komoditas apa saja yang saat ini menunjukkan anomali harga tertinggi (kritis) di luar kewajaran pergerakan rata-rata (Moving Average)?
2. Komoditas apa yang diprediksi oleh *Machine Learning* akan mengalami lonjakan harga terekstrem dalam 90 hari ke depan?

Proyek ini bertindak sebagai *painkiller*, bukan sekadar *vitamin*. Tanpa adanya sistem visibilitas data dan kecerdasan buatan, birokrasi sering kali bertindak reaktif saat harga sudah melambung. Solusi ini memberikan instrumen mitigasi proaktif yang siap pakai untuk menstabilkan perekonomian daerah sebelum inflasi terjadi melalui platform intelijen **Aceh Resilience Monitor (ARM)**.

---

### Deskripsi Project
**Nama Produk:** Aceh Resilience Monitor (ARM) - Dashboard Intelijen Harga Pangan  
**Fungsi:** Platform analitik *web-based* interaktif untuk mendeteksi anomali harga masa lalu dan memprediksi pergerakan harga 18 komoditas sembako esensial di Aceh hingga 3 bulan ke depan.  
**Penyelesaian Masalah:** ARM menyelesaikan masalah "keterlambatan respon" pemerintah. Alih-alih menyajikan tabel data yang rumit, ARM memberikan *Early Warning System* langsung berupa peringatan status "EKSTREM" atau "WASPADA", lengkap dengan rekomendasi tindakan preventif harian (misal: penyiapan kuota distribusi cadangan).

---

### Fitur Utama dan Teknologi yang Digunakan

**Fitur Utama:**
*   **Predictive Early Warning System (EWS) Cards:** Tampilan visual interaktif berupa kartu yang menyoroti 3 komoditas paling rentan mengalami lonjakan harga ekstrem dalam 90 hari ke depan.
*   **Actionable Insight AI (Meta Prophet):** Setiap kartu EWS secara otomatis menyertakan label bahaya (seperti EKSTREM atau WASPADA) beserta rekomendasi tindakan strategis konkret bagi pemerintah daerah.
*   **Historical Anomaly Detection:** Pendeteksian lonjakan harga tak wajar (*spikes*) berdasarkan perhitungan statistik Z-Score (simpangan baku) dan rata-rata bergerak 30 hari (MA30).
*   **Interactive Forecast Charts & YoY Analysis:** Visualisasi data interaktif per komoditas yang dilengkapi sakelar (*toggle*) untuk memunculkan garis tren masa lalu dan garis batas atas/bawah prediksi harga di masa depan.

**Teknologi & Tools:**
*   **Machine Learning (AI):** Meta Prophet (Algoritma utama untuk *Time-Series Forecasting* yang mampu menangani pola musiman data pangan).
*   **Data Processing:** Python, Pandas, Numpy (Untuk pembersihan data kotor, ETL, dan evaluasi metrik akurasi MAE/RMSE/MAPE).
*   **Layanan Cloud (Microsoft Azure):** 
    *   **Azure Blob Storage:** Digunakan sebagai arsitektur *Data Lake* ringan untuk menyimpan dan menyalurkan *dataset* hasil prediksi secara terpusat (*cloud storage*) agar langsung dapat dibaca oleh sistem visualisasi.
    *   **Azure Static Web Apps:** Digunakan untuk *deployment* aplikasi dasbor secara *serverless* agar mudah diakses oleh para pemangku kebijakan.
*   **Frontend:** HTML5, Vanilla CSS, Vanilla JavaScript (Chart.js v4).

---

### Cara Penggunaan Product
1.  **Akses Dasbor:** Pengguna (Pemerintah Daerah/Satgas Pangan) mengakses *link deployment* ARM melalui *browser* dari perangkat apa pun.
2.  **Membaca Prediksi EWS:** Di halaman utama, pengguna langsung disuguhkan panel **"Early Warning System (Meta Prophet AI)"** untuk melihat komoditas mana yang masuk daftar merah hari ini.
3.  **Tindakan Preventif:** Pengguna meninjau komoditas berstatus "EKSTREM" (misal: Prediksi kenaikan harga Cabai Merah sebesar >80%) dan dapat langsung merumuskan kebijakan stabilisasi harga hari itu juga.
4.  **Analisis Visual:** Pengguna menggulir ke bawah, memilih kategori komoditas (misal: Protein atau Sayur), mengklik tombol **"🔮 Tampilkan Prediksi 90 Hari"**, dan mengamati batas aman pergerakan harga komoditas tersebut.

---

### Rencana Pengembangan Lanjutan (Future Roadmap)
Meskipun prototipe ini sudah fungsional, ARM didesain agar dapat di-*scale up* ke level *Enterprise* pemerintah dengan rencana integrasi berikut:
*   **Fase 1 (Real-time Notifications):** Menghubungkan algoritma *Critical Anomaly* dengan API Bot Telegram/WhatsApp untuk mengirim peringatan *push notification* langsung ke gawai tim Satgas Pangan.
*   **Fase 2 (Correlation-Based Alerts):** Menerapkan peringatan dini rambatan inflasi (contoh: secara matematis sistem akan memperingatkan naiknya harga telur jika harga pakan unggas terdeteksi naik lebih dulu).
*   **Fase 3 (Multivariate AI):** Peningkatan model *Forecasting* dengan menyuntikkan data iklim sekunder (curah hujan dari BMKG) menggunakan Neural Networks untuk memprediksi ancaman gagal panen yang mengerek harga pasar.

---

### Tautan Penting
*   **Tautan Produk / Aplikasi (Microsoft Azure):** [https://thankful-river-084494910.7.azurestaticapps.net](https://thankful-river-084494910.7.azurestaticapps.net)
*   **Tautan Repositori GitHub:** [https://github.com/aceh-resilience-monitor/Aceh-Resilience-Monitor.git](https://github.com/aceh-resilience-monitor/Aceh-Resilience-Monitor.git)
*   **Laporan Dokumentasi & Analisis (Tersedia di Repositori):**
    *   **Evaluasi Metrik Model AI (Prophet):** `evaluation_prophet.md`
    *   **Eksplorasi Data (EDA) & Interpretasi Insight:** `docs/eda_interpretation.md`
    *   **Laporan Analisis Kualitas Data Awal:** `docs/data_analysis.md`
