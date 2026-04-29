### Project Brief Datathon
**Microsoft Elevate Training Center**

**Informasi Peserta**
*(Silakan isi tabel ini dengan nama dan email Dicoding kalian bertiga di dokumen asli)*
*   Aulia Muzhaffar (AI Engineer & Data Scientist)
*   Muhammad Ilhaam Ghiffary (Data Engineer & Frontend Developer)
*   Muhammad Arief Hidayah (Project Manager % Data Analyst)

**Topik:** Ketahanan Pangan & Agrikultur Modern
**Live Dashboard:** [https://thankful-river-084494910.7.azurestaticapps.net](https://thankful-river-084494910.7.azurestaticapps.net)

---

**Ringkasan Eksekutif**
Volatilitas harga pangan strategis sering kali memicu lonjakan inflasi daerah. Dalam praktiknya, pengambilan keputusan oleh pemangku kebijakan (seperti Tim Pengendalian Inflasi Daerah/TPID) sering terhambat oleh lambatnya integrasi data dan ketidakmampuan untuk memprediksi tren harga di masa depan berdasarkan data historis.

**Problem Statement:** Bagaimana menyatukan aliran data historis harga 18 komoditas pangan strategis untuk mendeteksi anomali secara *real-time* dan memprediksi lonjakan harga di masa depan guna memberikan rekomendasi intervensi pasar yang proaktif?

**Research Questions:** 
1. Komoditas apa saja yang saat ini menunjukkan anomali harga tertinggi (kritis) di luar kewajaran pergerakan rata-rata (Moving Average)?
2. Komoditas apa yang diprediksi oleh *Machine Learning* akan mengalami lonjakan harga terekstrem dalam 90 hari ke depan?

Proyek ini bertindak sebagai *painkiller*, bukan sekadar *vitamin*. Tanpa adanya sistem visibilitas data dan kecerdasan buatan, birokrasi sering kali bertindak reaktif saat harga sudah melambung. Solusi ini memberikan instrumen mitigasi proaktif yang siap pakai untuk menstabilkan perekonomian daerah sebelum inflasi terjadi.

---

**Deskripsi Project**
Aceh Resilience Monitor (ARM) adalah sebuah platform intelijen bisnis *end-to-end* yang dirancang untuk mendeteksi anomali dan melakukan *forecasting* harga pada 18 komoditas pangan strategis di Provinsi Aceh.

Fungsi utama produk ini adalah memproses data harga historis (2023-2025), mendeteksi simpangan anomali statistik, dan meramalkan tren menggunakan *Machine Learning*. ARM menyelesaikan masalah kelambatan birokrasi dengan mengubah data tersebut menjadi "Early Warning System (Sistem Peringatan Dini)" yang memberikan rekomendasi intervensi pasar secara instan di layar pembuat kebijakan.

---

**Fitur Utama dan Teknologi yang Digunakan**

*   **Automated ETL Pipeline (Python & Pandas):** Skrip pemrosesan data otomatis untuk membersihkan dan menstrukturisasi jutaan baris data harga mentah harian menjadi dataset siap analisis.
*   **Time-Series Forecasting & Anomaly Detection (Meta Prophet):** Implementasi model *Machine Learning* untuk mendeteksi lonjakan harga abnormal (menggunakan perhitungan *Z-Score*) dan memprediksi pergerakan harga 18 komoditas selama 90 hari ke depan secara akurat (MAPE 7.74%).
*   **Cloud Data Lake (Azure Blob Storage):** Infrastruktur penyimpanan *cloud-native* terpusat yang telah diimplementasikan secara penuh untuk mendistribusikan *output* data JSON hasil prediksi AI langsung ke *frontend* aplikasi secara dinamis (dengan konfigurasi CORS terpusat).
*   **Real-time Executive Dashboard (HTML, JS, Chart.js):** Visualisasi data premium berdesain *glassmorphism* interaktif tanpa *latency*, menyajikan metrik tren, volatilitas, dan perbandingan YoY (*Year-over-Year*).
*   **Predictive Early Warning System (Vanilla JS Logic):** Panel peringatan interaktif berbasis probabilitas AI yang secara otomatis menyortir dan menyoroti komoditas dengan prediksi lonjakan harga ekstrem (misal: >15%), lengkap dengan rekomendasi tindakan.
*   **Cloud Hosting (Azure Static Web Apps):** *Deployment dashboard* yang *scalable*, aman, dan dapat diakses dari peramban mana pun secara global.

---

**Cara Penggunaan Product**

1.  Pengguna (Pemangku kebijakan/TPID) membuka tautan *dashboard* ARM melalui peramban web (*browser*).
2.  Pada bagian atas halaman, pengguna langsung disambut oleh panel **"Early Warning System"** yang menyoroti Top 3 komoditas dengan prediksi lonjakan harga terekstrem di masa depan (dilengkapi label 🔴 EKSTREM atau 🟡 WASPADA).
3.  Pengguna dapat mengklik tombol **"Lihat Semua Prediksi"** untuk membuka modal/tabel detail yang membandingkan harga saat ini dengan harga prediksi AI 90 hari ke depan.
4.  Menggulir ke bawah, pengguna melihat **Grid Status Komoditas** yang memantau kondisi terkini 18 komoditas (Aman/Waspada/Kritis) berdasarkan anomali harian (*Z-Score*).
5.  Pengguna dapat memanfaatkan grafik interaktif (Tren Harga, Kontribusi Kategori) untuk menganalisis pergerakan pasar secara *drill-down* menggunakan filter kategori di layar.

---

**Informasi Pendukung [Opsional]**

**Studi Kasus Pengguna:** Menjelang periode kuartal pertama 2026, TPID Provinsi Aceh perlu mengantisipasi inflasi. Saat membuka *dashboard* ARM, sistem EWS (*Early Warning System*) mengeluarkan peringatan 🔴 EKSTREM untuk komoditas Cabai Merah karena model *Prophet* memprediksi adanya anjakan harga hingga +80.4% dalam 90 hari ke depan. Berbekal rekomendasi "Siapkan stok cadangan" yang tertera di *dashboard*, dinas terkait langsung menjadwalkan inspeksi rantai pasok keesokan paginya jauh sebelum harga cabai benar-benar meledak di pasar.

**Rencana pengembangan ke depan:** Mengintegrasikan data eksternal seperti anomali cuaca lokal (curah hujan) dan indeks harga BBM sebagai regressor tambahan dalam model prediksi *Prophet* untuk meningkatkan akurasi visibilitas terhadap potensi gagal panen atau kendala logistik.
