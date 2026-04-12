# 📊 Interpretasi EDA — Harga Bahan Pokok Harian (2023–2025)

Semua 13 plot tersimpan di folder `plots/`. Berikut interpretasi lengkap tiap visualisasi.

---

## Plot 1 — Box Plots: Distribusi Harga per Komoditas & Tahun
![Box Plots](/plots/01_boxplots.png)

### Temuan Utama:
- **Daging Sapi** adalah komoditas termahal (~Rp 150K–180K), outliernya sangat tinggi dan terpisah jauh dari komoditas lainnya.
- **Cabai Merah Keriting & Cabai Rawit Hijau** memiliki *whisker* (rentang) paling lebar — variabilitas harga sangat tinggi, terutama di 2025 (box melebar).
- **Beras semua kualitas** termasuk low-price group (~Rp 12K–17K), dan terlihat adanya **kenaikan konsisten** tiap tahun — box 2025 lebih tinggi dari 2024, lalu lebih tinggi dari 2023.
- **Minyak Goreng Kemasan Bermerk 1** paling stabil — box sangat sempit dan hampir tidak bergeser antar tahun.
- Outlier (titik) paling banyak muncul di **Daging Sapi** dan **Cabai Rawit Hijau**, menandakan lonjakan harga yang episodik.

---

## Plot 2 — Violin Plots: Distribusi Komoditas Paling Volatil
![Violin Plots](/plots/02_violin_volatile.png)

### Temuan Utama:
- **Cabai Merah Keriting 2025**: Distribusi sangat melebar ke atas (sampai >140K), menunjukkan terjadi lonjakan harga yang ekstrem. Bentuk violin *bimodal* — ada dua puncak, satu di ~30K dan satu di ~80K.
- **Cabai Rawit Hijau**: Pola serupa, tapi tahun 2023 punya distribusi yang lebih tersebar dibandingkan 2024 yang lebih terkonsentrasi.
- **Bawang Merah**: Di tahun 2024, distribusi sangat lebar (sampai 65K), menandakan episode price shock besar di tahun tersebut.
- **Daging Ayam**: Pola yang menarik — violin melebar setiap tahun, median 2025 secara jelas lebih tinggi (~37K vs ~28K di 2023). Tren kenaikan yang jelas.

---

## Plot 3 — Time Series Semua Komoditas per Kategori
![Time Series](/plots/03_timeseries_all.png)

### Temuan Utama:
- **Bawang Merah**: Pola *cyclical* yang sangat jelas — ada puncak-puncak harga yang berulang setiap ~6 bulan.
- **Bawang Putih**: Relatif stabil di 2023, terjadi lonjakan tajam di mid-2024 (naik ke ~47K), lalu kembali turun. Pola serupa terulang di late 2025.
- **Beras**: Semua 6 varian beras menunjukkan **regime change** yang jelas di awal 2024 — harga naik secara *step-function* (loncatan sekaligus, bukan gradual), lalu stabil di level baru yang lebih tinggi.
- **Cabai Merah Keriting**: Pola paling "liar" — ada spike ke >140K di late 2025, yang merupakan **rekor tertinggi** selama 3 tahun.
- **Cabai Rawit Hijau**: Pola cyclical mirip Cabai Merah, dengan spike di mid-2024 (~90K).
- **Daging Ayam**: Tren naik bertahap yang cukup *steady*, tanpa spike dramatis.
- **Daging Sapi**: Cukup stabil di atas Rp 150K. Ada spike Lebaran (Mar-Apr 2023) ke ~178K.
- **Gula Pasir**: Kenaikan *step-wise* — naik per "level" dan bertahan. Gula Premium dan Lokal bergerak paralel.
- **Minyak Goreng**: Minyak Goreng Curah menunjukkan kenaikan paling dramatis (dari ~16K ke ~22K), sementara yang Bermerk relatif stabil.
- **Telur Ayam**: Spike besar di late 2025 — harga naik dari ~30K ke ~58K.

---

## Plot 4 — Komoditas Volatil dengan 30-Day Moving Average
![Volatile MA](/plots/04_volatile_ma30.png)

### Temuan Utama:
- **Cabai Merah Keriting**: MA30 menunjukkan 5 siklus harga dalam 3 tahun. Siklus terakhir (Q4 2025) adalah yang paling tinggi (~80K MA, dengan daily peak >140K). Tren baseline naik dari ~40K ke ~60K.
- **Cabai Rawit Hijau**: Siklus yang lebih reguler — puncak di Jul 2023, Apr 2024, Jun 2024, dan Nov 2025. Baseline cukup stabil di ~45K.
- **Bawang Merah**: MA30 mengkonfirmasi 4 major peaks: May 2023, Apr 2024, Jul 2024, Aug 2025. Pola seasonal yang terkait musim panen (harga turun setelah panen, naik sebelumnya).

---

## Plot 5 — Total Perubahan Harga 2023→2025
![Total Change](/plots/05_total_change_bar.png)

### Temuan Utama:
- **5 Komoditas naik di atas 20%** (merah, di atas threshold):
  1. **Minyak Goreng Curah**: +29.5% — kenaikan terbesar!
  2. **Daging Ayam Ras Segar**: +29.3%
  3. **Cabai Merah Keriting**: +24.9%
  4. **Bawang Merah Ukuran Sedang**: +23.9%
  5. **Gula Pasir Kualitas Premium**: +21.2%
- **Daging Sapi Kualitas 1**: Satu-satunya komoditas yang **turun** (-0.2%), menunjukkan harga sapi relatif stabil/sedikit menurun.
- **Semua varian Beras** naik 16–19%, yang cukup signifikan mengingat beras adalah kebutuhan pokok utama.
- **Minyak Goreng Kemasan Bermerk 1**: Hanya naik +4%, menandakan harga terproteksi/terkontrol.

> [!IMPORTANT]
> Kenaikan >20% dalam 2 tahun menandakan **inflasi harga pangan yang signifikan**, terutama pada minyak goreng curah dan protein hewani.

---

## Plot 6 — Perbandingan Kenaikan Year-over-Year
![YoY Comparison](/plots/06_yoy_comparison.png)

### Temuan Utama:
- **Pola umum**: Kenaikan 2023→2024 (biru) umumnya **lebih besar** dari 2024→2025 (merah) untuk mayoritas komoditas. Ini menandakan laju inflasi harga melambat di 2025.
- **Pengecualian penting**:
  - **Cabai Merah Keriting**: Naik lebih besar di 2024→2025 (+18%) dibanding 2023→2024 (+5.7%), artinya akselerasi harga.
  - **Minyak Goreng Kemasan Bermerk 2**: Turun di 2023→2024 tapi naik +11% di 2024→2025.
- **Cabai Rawit Hijau**: +14% di 2023→2024 tapi turun tipis di 2024→2025, menandakan konsolidasi harga.
- **Gula Pasir**: Lonjakan besar di 2023→2024 (+17%), melambat di 2024→2025 (+2–3%).

---

## Plot 7 — Heatmap Volatilitas (Coefficient of Variation)
![CV Heatmap](/plots/07_cv_heatmap.png)

### Temuan Utama:
- **Cabai Merah Keriting** adalah yang PALING volatil — CV naik tiap tahun: 25.9% → 31.6% → **35.5%**. Ini sangat tinggi.
- **Cabai Rawit Hijau**: CV 22.7% di 2023, turun di 2024 (13.8%), naik lagi di 2025 (22.0%).
- **Bawang Merah**: Lonjakan volatilitas di 2024 (CV 24.9%), artinya ada disrupsi supply besar di tahun itu.
- **Telur Ayam**: Volatilitas melonjak drastis di 2025 (CV 15.1% vs 4.9% di 2024) — kemungkinan terkait spike harga di Q4 2025.
- **Daging Sapi Kualitas 1**: Paling stabil secara konsisten (CV 2.7%, 0.7%, 2.1%).
- **Minyak Goreng Kemasan Bermerk 1**: Juga sangat stabil (CV ~1.4–2.9%), menunjukkan harga yang terkontrol pasar/pemerintah.

---

## Plot 8 — Matriks Korelasi Harga
![Correlation Matrix](/plots/08_correlation_matrix.png)

### Temuan Utama:
- **Cluster yang sangat kuat (r > 0.95)**:
  - Semua **varian Beras** berkorelasi 0.96–0.99 satu sama lain → mereka bergerak serentak.
  - **Gula Pasir Premium & Lokal**: r = 0.94.
  - **Minyak Goreng Kemasan 1 & 2**: r = 0.94.
- **Korelasi tinggi lintas kategori**:
  - **Gula Pasir & Beras**: r = 0.85–0.90 → kenaikan harga beras diikuti kenaikan gula, kemungkinan karena faktor makroekonomi (inflasi umum, biaya distribusi).
  - **Minyak Goreng Curah & Gula Pasir**: r = 0.82–0.85 → lagi-lagi menandakan *co-movement* harga bahan pokok utama.
- **Korelasi rendah/tidak berkorelasi**:
  - **Cabai Merah & Cabai Rawit**: r = 0.51. Menariknya, meskipun keduanya "cabai", mereka tidak bergerak identik.
  - **Bawang Merah** hampir independen dari semua komoditas (r = 0.10–0.41), dipengaruhi oleh faktor supply-nya sendiri.
- **Korelasi negatif**:
  - **Daging Sapi** vs Beras/Gula: r ≈ -0.11 s/d -0.15. Ketika beras/gula naik, daging sapi cenderung sedikit turun.

---

## Plot 9 — Pola Seasonalitas Bulanan
![Seasonality](/plots/09_seasonality.png)

### Temuan Utama:
- **Cabai Merah Keriting**: Puncak di Feb-Mar dan Aug-Sep. Trough di Sep-Oct (musim panen besar cabai). Tahun 2025 sangat anomali — harga melonjak tajam di Q4.
- **Cabai Rawit Hijau**: Peak di Jan-Feb dan Aug-Sep, trough di Apr-Jun. Tahun 2025 menunjukkan harga Dec terbang ke ~67K.
- **Bawang Merah**: Seasonal pattern kuat — peak di Apr-May (sebelum musim panen), trough di Sep-Oct (musim panen).
- **Daging Ayam**: Peak di Dec (Natal & Tahun Baru). Tahun 2025 sangat menonjol — harga Dec mencapai >42K, tertinggi sepanjang 3 tahun.
- **Telur Ayam**: Mirip Daging Ayam, peak di Dec. Tahun 2025 punya outlier masif di Dec (~40K vs normal ~29K).
- **Bawang Putih**: Peak di Jul-Aug, trough di Jan-Feb. Kemungkinan terkait siklus impor.

---

## Plot 10 — Heatmap Seasonalitas Z-Score
![Z-Score Heatmap](/plots/10_zscore_heatmap.png)

### Temuan Utama:
- **Pola "mahal di akhir tahun"**: Hampir semua komoditas berwarna merah (Z-score tinggi) di **Oct-Nov-Dec**, terutama:
  - **Minyak Goreng Curah**: Dec = +2.80 (sangat tinggi)
  - **Minyak Goreng Kemasan 1 & 2**: Dec = +2.77
  - **Telur Ayam**: Dec = +2.84 (tertinggi)
  - **Beras semua kualitas**: Nov-Dec = +1.0 s/d +1.72
- **Pola "murah di awal tahun"**: Jan-Feb-Mar umumnya berwarna hijau (Z-score rendah), terutama:
  - **Gula Pasir Premium**: Jan = -1.97
  - **Bawang Putih**: Jan-Feb = -1.67, -1.62
- **Daging Sapi** punya pola unik: lonjakan besar **hanya di Maret** (Z = +2.82) — ini adalah efek **Ramadan/Lebaran** yang sangat presisi.
- **Bawang Merah**: Peak di May (+1.49), trough di Oct (-1.79) — cerminkan siklus panen.

> [!TIP]
> Pola seasonality ini sangat berharga untuk model prediksi — bulan tertentu secara konsisten lebih mahal/murah.

---

## Plot 11 — Distribusi Return Harian
![Daily Returns](/plots/11_daily_returns.png)

### Temuan Utama:
- **Cabai Merah Keriting**: σ = 8.06% — standar deviasi return harian tertinggi. Distribusi memiliki **ekor kanan yang sangat panjang** (sampai +100%!), menandakan satu hari bisa naik 2x lipat.
- **Cabai Rawit Hijau**: σ = 5.98%, serupa tapi sedikit lebih rendah. Juga punya fat right tail.
- **Bawang Merah**: σ = 3.29%, distribusi lebih simetris tapi tetap leptokurtic (puncak tinggi, ekor tebal).
- **Telur Ayam, Daging Ayam, Bawang Putih**: σ ≈ 1.8–2.1%, jauh lebih rendah. Distribusi lebih terpusat di 0.
- Semua komoditas memiliki **mean return positif** (0.03–0.26%), menandakan tren inflasi harian yang kecil tapi konsisten.

> [!WARNING]
> Fat tails di Cabai Merah/Rawit menandakan risiko harga ekstrem — ini sulit di-predict dengan model distribusi normal.

---

## Plot 12 — Harga Rata-rata per Kategori & Tahun
![Category Prices](/plots/12_category_prices.png)

### Temuan Utama:
- **Daging Sapi** mendominasi skala harga (~Rp 150K), 3x lipat dari kategori ke-2.
- **Kenaikan paling visible per tahun**: Beras, Gula Pasir, Daging Ayam — bar hijau (2025) konsisten lebih panjang dari bar pink (2023).
- **Minyak Goreng & Gula Pasir**: Kategori "termurah", tapi justru minyak goreng curah punya persentase kenaikan tertinggi (+29.5%).
- **Bawang Merah & Bawang Putih**: Harga absolut serupa (~Rp 35–42K), tapi Bawang Putih lebih stabil antar tahun.

---

## Plot 13 — Stacked Area Chart: Kontribusi Kategori terhadap Total Harga
![Stacked Area](/plots/13_stacked_area.png)

### Temuan Utama:
- **Total combined price naik ~30%**: dari ~Rp 270K (Jan 2023) ke ~Rp 350K+ (Nov 2025).
- **Bawang Putih & Bawang Merah** (kuning & hijau di bawah) memberikan kontribusi fluktuasi besar — terlihat dari "gelombang" di area bawah.
- **Cabai (Merah + Rawit)** adalah **driver utama variabilitas** — area pink/ungu berfluktuasi paling lebar. Peak di Mar 2024 terlihat sangat jelas.
- **Beras** (biru gelap) menunjukkan jump yang jelas di awal 2024, setelah itu **sustained** di level yang lebih tinggi.
- **Minyak Goreng** (coklat) naik secara gradual tapi konsisten.
- Ada pola seasonal berulang — combined price cenderung puncak di Dec/Jan setiap tahun.

---

## 🔑 Ringkasan Temuan Kunci

| Insight | Detail |
|---------|--------|
| **Komoditas paling inflasioner** | Minyak Goreng Curah (+29.5%), Daging Ayam (+29.3%) |
| **Komoditas paling volatil** | Cabai Merah Keriting (CV 31%), Cabai Rawit Hijau (CV 19%) |
| **Komoditas paling stabil** | Daging Sapi (CV 2%), Minyak Goreng Kemasan 1 (CV 2%) |
| **Efek Ramadan/Lebaran** | Daging Sapi naik tajam HANYA di bulan Maret (Z = +2.82) |
| **Efek Natal/Tahun Baru** | Telur Ayam & Daging Ayam peak di Desember |
| **Regime change** | Beras mengalami jump harga di awal 2024 dan tidak kembali |
| **Korelasi terkuat** | Semua varian Beras (r > 0.96); Gula Premium & Lokal (r = 0.94) |
| **Anomali 2025** | Cabai Merah Keriting melonjak ke >Rp 140K di Q4 — rekor tertinggi |

> [!NOTE]
> Semua plot disimpan di folder `/plots/` sebagai file PNG resolusi tinggi (150 DPI).
