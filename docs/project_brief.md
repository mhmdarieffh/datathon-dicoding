
Project Brief Datathon
Microsoft Elevate Training Center

Informasi Peserta
(Silakan isi tabel ini dengan nama dan email Dicoding kalian bertiga di dokumen asli)

Topik : Ketahanan Pangan & Agrikultur Modern

Ringkasan Eksekutif
Volatilitas harga pangan strategis sering kali memicu lonjakan inflasi daerah. Dalam praktiknya, pengambilan keputusan oleh pemangku kebijakan (seperti Tim Pengendalian Inflasi Daerah/TPID) sering terhambat oleh lambatnya integrasi data yang tersebar (silo) antara pusat informasi harga seperti PIHPS dan SP2KP.

Problem Statement: Bagaimana menyatukan aliran data disparitas harga komoditas secara real-time untuk mendeteksi anomali dan memberikan rekomendasi intervensi pasar yang tepat sasaran di kawasan perkotaan?

Research Questions: 1. Komoditas apa saja yang menunjukkan anomali harga tertinggi di luar tren musiman normal?
2. Kapan dan di pasar mana intervensi (seperti operasi pasar murah) harus segera dilakukan sebelum inflasi bulanan tidak terkendali?

Proyek ini bertindak sebagai painkiller, bukan sekadar vitamin. Tanpa adanya sistem visibilitas data yang terpusat dan otomatis, birokrasi pemerintahan sering kali terlambat menyadari lonjakan harga hingga dampaknya sudah memukul daya beli masyarakat. Solusi ini memberikan instrumen mitigasi proaktif yang siap pakai untuk menstabilkan perekonomian daerah.

Deskripsi Project
Aceh Resilience Monitor (ARM) adalah sebuah platform intelijen bisnis end-to-end yang dirancang untuk mendeteksi anomali harga pangan strategis di pasar-pasar utama.

Fungsi utama produk ini adalah menyedot data dari berbagai portal pemerintah, memprosesnya dalam satu "danau data" terpusat, dan menyajikan metrik peringatan dini. ARM menyelesaikan masalah kelambatan respons birokrasi dengan mengubah data mentah harian menjadi sinyal eksekusi intervensi pasar yang instan.

Fitur Utama dan Teknologi yang Digunakan

Automated Data Pipeline (Microsoft Fabric - Data Factory): Penarikan data otomatis secara berkala dari API PIHPS dan SP2KP tanpa intervensi manual.

Single Source of Truth Storage (Microsoft Fabric - OneLake): Penyimpanan data berformat Delta Parquet untuk efisiensi pemrosesan tingkat lanjut.

Price Anomaly Detection (Synapse Data Science): Implementasi algoritma machine learning untuk mendeteksi lonjakan harga yang tidak wajar (di luar batas toleransi statistik).

Real-time Executive Dashboard (Power BI DirectLake): Visualisasi sebaran harga per pasar tanpa loading latency, dirancang khusus untuk layar pembuat kebijakan.

Automated Early Warning System (Data Activator): Pengiriman notifikasi otomatis ketika harga komoditas menyentuh ambang batas kritis.

Cara Penggunaan Product

Pengguna (Pemangku kebijakan/Dinas terkait) membuka link dashboard ARM melalui peramban web.

Pada halaman utama, pengguna langsung melihat peta kota dengan titik-titik pasar (misal: Pasar Peunayong, Pasar Lambaro) yang memiliki indikator warna (Hijau: Aman, Kuning: Waspada, Merah: Kritis).

Pengguna mengklik pasar dengan indikator "Merah" untuk melihat komoditas apa yang memicu peringatan (contoh: Cabai Merah).

Pengguna melihat grafik proyeksi dan anomali, lalu menggunakan tombol "Ekspor Laporan" untuk membagikan data tersebut sebagai dasar rapat operasi pasar hari itu.

Secara paralel, jika pengguna tidak sedang membuka dashboard, sistem akan otomatis mengirimkan peringatan via email/Microsoft Teams apabila terjadi anjakan harga harian yang drastis.

Informasi Pendukung [Opsional]

Studi Kasus Pengguna: Menjelang hari besar keagamaan, TPID Kota Banda Aceh perlu memantau pergerakan harga daging sapi dan bawang merah. Melalui notifikasi ARM, TPID mengetahui adanya lonjakan harga 15% di Pasar Aceh dalam 2 hari terakhir, sehingga langsung menjadwalkan inspeksi rantai pasok keesokan paginya.

Rencana pengembangan ke depan: Mengintegrasikan data anomali cuaca lokal (curah hujan) sebagai variabel tambahan dalam model forecasting untuk memprediksi potensi gagal panen di daerah pemasok.
