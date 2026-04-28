"""
Prepare dashboard data from Excel commodity price files.
Outputs dashboard/dashboard_data.json for the ARM web dashboard.
Run from project root: .venv/bin/python scripts/prepare_dashboard_data.py
"""
import pandas as pd
import numpy as np
import json
import os
import logging
from pathlib import Path
from prophet import Prophet

# Silence prophet logging
logging.getLogger('prophet').setLevel(logging.ERROR)
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

# Resolve project root (one level up from scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DASHBOARD_DIR = PROJECT_ROOT / 'dashboard'

# ── Load & Clean (reused from save_plots.py) ──────────────────────
CATEGORY_MAP = {
    'Beras Kualitas Bawah I': 'Beras',
    'Beras Kualitas Bawah II': 'Beras',
    'Beras Kualitas Medium I': 'Beras',
    'Beras Kualitas Medium II': 'Beras',
    'Beras Kualitas Super I': 'Beras',
    'Beras Kualitas Super II': 'Beras',
    'Daging Ayam Ras Segar': 'Daging Ayam',
    'Daging Sapi Kualitas 1': 'Daging Sapi',
    'Telur Ayam Ras Segar': 'Telur Ayam',
    'Bawang Merah Ukuran Sedang': 'Bawang Merah',
    'Bawang Putih Ukuran Sedang': 'Bawang Putih',
    'Cabai Merah Keriting': 'Cabai Merah',
    'Cabai Rawit Hijau': 'Cabai Rawit',
    'Minyak Goreng Curah': 'Minyak Goreng',
    'Minyak Goreng Kemasan Bermerk 1': 'Minyak Goreng',
    'Minyak Goreng Kemasan Bermerk 2': 'Minyak Goreng',
    'Gula Pasir Kualitas Premium': 'Gula Pasir',
    'Gula Pasir Lokal': 'Gula Pasir',
}

# Short display names for the dashboard
SHORT_NAMES = {
    'Beras Kualitas Bawah I': 'Beras Bawah I',
    'Beras Kualitas Bawah II': 'Beras Bawah II',
    'Beras Kualitas Medium I': 'Beras Medium I',
    'Beras Kualitas Medium II': 'Beras Medium II',
    'Beras Kualitas Super I': 'Beras Super I',
    'Beras Kualitas Super II': 'Beras Super II',
    'Daging Ayam Ras Segar': 'Daging Ayam',
    'Daging Sapi Kualitas 1': 'Daging Sapi',
    'Telur Ayam Ras Segar': 'Telur Ayam',
    'Bawang Merah Ukuran Sedang': 'Bawang Merah',
    'Bawang Putih Ukuran Sedang': 'Bawang Putih',
    'Cabai Merah Keriting': 'Cabai Merah',
    'Cabai Rawit Hijau': 'Cabai Rawit',
    'Minyak Goreng Curah': 'M. Goreng Curah',
    'Minyak Goreng Kemasan Bermerk 1': 'M. Goreng Merk 1',
    'Minyak Goreng Kemasan Bermerk 2': 'M. Goreng Merk 2',
    'Gula Pasir Kualitas Premium': 'Gula Premium',
    'Gula Pasir Lokal': 'Gula Lokal',
}

CATEGORY_ICONS = {
    'Beras': '🍚',
    'Daging Ayam': '🍗',
    'Daging Sapi': '🥩',
    'Telur Ayam': '🥚',
    'Bawang Merah': '🧅',
    'Bawang Putih': '🧄',
    'Cabai Merah': '🌶️',
    'Cabai Rawit': '🫑',
    'Minyak Goreng': '🫗',
    'Gula Pasir': '🍬',
}


def load_and_clean(filepath, year):
    """Load Excel file and return clean DataFrame."""
    raw = pd.read_excel(filepath, header=None)
    date_strings = raw.iloc[0, 2:].values
    dates = pd.to_datetime(date_strings, format='%d/ %m/ %Y')
    roman_numerals = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'}
    data_rows = raw.iloc[1:]
    mask = ~data_rows.iloc[:, 0].isin(roman_numerals)
    commodity_data = data_rows[mask].copy()
    records = []
    for _, row in commodity_data.iterrows():
        commodity_name = row.iloc[1].strip()
        prices = row.iloc[2:].values
        for date, price in zip(dates, prices):
            price_str = str(price).strip()
            if pd.isna(price) or price_str in ('', '-', 'nan'):
                price_val = np.nan
            else:
                price_val = float(price_str.replace(',', ''))
            records.append({
                'date': date,
                'commodity': commodity_name,
                'price': price_val,
                'year': year
            })
    return pd.DataFrame(records)


print('Loading data...')
df = pd.concat([load_and_clean(DATA_DIR / f'{y}.xlsx', y) for y in [2023, 2024, 2025]], ignore_index=True)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['category'] = df['commodity'].map(CATEGORY_MAP)
df_clean = df.dropna(subset=['price']).copy()
print(f'Loaded {len(df_clean):,} clean records')

commodities = sorted(df_clean['commodity'].unique())

# ── 1. Time Series Data (sampled to weekly for performance) ──────
print('Preparing time series data...')
timeseries = {}
for commodity in commodities:
    cdf = df_clean[df_clean['commodity'] == commodity].sort_values('date')
    # Weekly resample for lighter JSON
    weekly = cdf.set_index('date')['price'].resample('W').mean().dropna()
    timeseries[commodity] = {
        'dates': [d.strftime('%Y-%m-%d') for d in weekly.index],
        'prices': [round(p, 0) for p in weekly.values],
        'category': CATEGORY_MAP[commodity],
        'shortName': SHORT_NAMES[commodity],
    }

# Also keep daily for the most recent 90 days for anomaly detail
latest_date = df_clean['date'].max()
recent_start = latest_date - pd.Timedelta(days=90)
timeseries_daily_recent = {}
for commodity in commodities:
    cdf = df_clean[(df_clean['commodity'] == commodity) & (df_clean['date'] >= recent_start)].sort_values('date')
    timeseries_daily_recent[commodity] = {
        'dates': [d.strftime('%Y-%m-%d') for d in cdf['date']],
        'prices': [round(p, 0) for p in cdf['price']],
    }

# ── 2. Anomaly Detection (beyond 2σ from 30-day MA) ──────────────
print('Detecting anomalies...')
anomalies = []
for commodity in commodities:
    cdf = df_clean[df_clean['commodity'] == commodity].sort_values('date').copy()
    cdf = cdf.set_index('date')
    cdf['ma30'] = cdf['price'].rolling('30D').mean()
    cdf['std30'] = cdf['price'].rolling('30D').std()
    cdf = cdf.dropna(subset=['ma30', 'std30'])
    cdf['z_score'] = (cdf['price'] - cdf['ma30']) / cdf['std30']

    # Flag anomalies: |z| > 2
    anomaly_rows = cdf[cdf['z_score'].abs() > 2]
    for date_idx, row in anomaly_rows.iterrows():
        deviation_pct = ((row['price'] - row['ma30']) / row['ma30'] * 100)
        severity = 'critical' if abs(row['z_score']) > 3 else 'warning'
        anomalies.append({
            'date': date_idx.strftime('%Y-%m-%d'),
            'commodity': commodity,
            'shortName': SHORT_NAMES[commodity],
            'category': CATEGORY_MAP[commodity],
            'price': round(row['price'], 0),
            'ma30': round(row['ma30'], 0),
            'deviation_pct': round(deviation_pct, 1),
            'z_score': round(row['z_score'], 2),
            'severity': severity,
        })

# Sort by date descending
anomalies.sort(key=lambda x: x['date'], reverse=True)
print(f'  Found {len(anomalies)} anomaly events')

# ── 3. Commodity Status Cards ────────────────────────────────────
print('Computing commodity status...')
yearly_mean = df_clean.groupby(['year', 'commodity'])['price'].mean().unstack(level=0)
total_change = ((yearly_mean[2025] - yearly_mean[2023]) / yearly_mean[2023] * 100)

# CV for most recent year (2025)
cv_2025 = df_clean[df_clean['year'] == 2025].groupby('commodity')['price'].agg(
    lambda x: x.std() / x.mean() * 100
)

# Latest price (last available date)
latest_prices = df_clean[df_clean['date'] == df_clean['date'].max()].set_index('commodity')['price']

# Previous month average
prev_month_start = latest_date - pd.Timedelta(days=30)
prev_month_avg = df_clean[
    (df_clean['date'] >= prev_month_start) & (df_clean['date'] <= latest_date)
].groupby('commodity')['price'].mean()

commodity_cards = []
for commodity in commodities:
    cv = cv_2025.get(commodity, 0)
    change = total_change.get(commodity, 0)
    price = latest_prices.get(commodity, 0)
    prev_avg = prev_month_avg.get(commodity, price)
    month_change = ((price - prev_avg) / prev_avg * 100) if prev_avg else 0

    # Status logic
    if cv > 15 or abs(change) > 20:
        status = 'critical'
    elif cv > 5 or abs(change) > 10:
        status = 'warning'
    else:
        status = 'normal'

    # Count anomalies in recent 90 days for this commodity
    recent_anomaly_count = len([
        a for a in anomalies
        if a['commodity'] == commodity and a['date'] >= recent_start.strftime('%Y-%m-%d')
    ])

    commodity_cards.append({
        'commodity': commodity,
        'shortName': SHORT_NAMES[commodity],
        'category': CATEGORY_MAP[commodity],
        'icon': CATEGORY_ICONS.get(CATEGORY_MAP[commodity], '📦'),
        'latestPrice': round(price, 0),
        'monthChange': round(month_change, 1),
        'totalChange': round(change, 1),
        'cv2025': round(cv, 1),
        'status': status,
        'recentAnomalies': recent_anomaly_count,
    })

# ── 4. YoY Changes ──────────────────────────────────────────────
print('Computing YoY changes...')
change_23_24 = ((yearly_mean[2024] - yearly_mean[2023]) / yearly_mean[2023] * 100)
change_24_25 = ((yearly_mean[2025] - yearly_mean[2024]) / yearly_mean[2024] * 100)

yoy_data = []
for commodity in commodities:
    yoy_data.append({
        'commodity': commodity,
        'shortName': SHORT_NAMES[commodity],
        'category': CATEGORY_MAP[commodity],
        'change_23_24': round(change_23_24.get(commodity, 0), 1),
        'change_24_25': round(change_24_25.get(commodity, 0), 1),
        'total_change': round(total_change.get(commodity, 0), 1),
    })

yoy_data.sort(key=lambda x: x['total_change'], reverse=True)

# ── 5. Seasonality Z-Scores ─────────────────────────────────────
print('Computing seasonality Z-scores...')
monthly_pivot = df_clean.groupby(['commodity', 'month'])['price'].mean().unstack()
monthly_normalized = monthly_pivot.apply(lambda x: (x - x.mean()) / x.std(), axis=1)

seasonality_data = {}
for commodity in commodities:
    if commodity in monthly_normalized.index:
        row = monthly_normalized.loc[commodity]
        seasonality_data[commodity] = {
            'shortName': SHORT_NAMES[commodity],
            'values': [round(v, 2) if not pd.isna(v) else 0 for v in row.values],
        }

# ── 6. Volatility Heatmap Data ───────────────────────────────────
print('Computing volatility data...')
cv_all = df_clean.groupby(['year', 'commodity'])['price'].agg(
    lambda x: x.std() / x.mean() * 100
).unstack(level=0).round(1)

volatility_data = {}
for commodity in commodities:
    if commodity in cv_all.index:
        volatility_data[commodity] = {
            'shortName': SHORT_NAMES[commodity],
            'category': CATEGORY_MAP[commodity],
            '2023': round(cv_all.loc[commodity, 2023], 1) if 2023 in cv_all.columns else 0,
            '2024': round(cv_all.loc[commodity, 2024], 1) if 2024 in cv_all.columns else 0,
            '2025': round(cv_all.loc[commodity, 2025], 1) if 2025 in cv_all.columns else 0,
        }

# ── 7. Correlation Data ─────────────────────────────────────────
print('Computing correlations...')
price_wide = df_clean.pivot_table(index='date', columns='commodity', values='price')
corr = price_wide.corr().round(2)
correlation_data = {
    'commodities': [SHORT_NAMES[c] for c in corr.columns],
    'matrix': corr.values.tolist(),
}

# ── 8. Price Forecasting (Prophet) ───────────────────────────────
print('Generating 90-day forecasts...')
forecasts = {}
future_anomalies = []

for commodity in commodities:
    try:
        # Prepare data for Prophet
        cdf = df_clean[df_clean['commodity'] == commodity].sort_values('date').copy()
        pdf = cdf[['date', 'price']].rename(columns={'date': 'ds', 'price': 'y'})
        
        # Initialize and fit model
        # yearly_seasonality = True because food prices often follow holiday cycles
        model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        model.fit(pdf)
        
        # Predict 90 days
        future = model.make_future_dataframe(periods=90)
        forecast = model.predict(future)
        
        # Extract only the future part
        future_data = forecast[forecast['ds'] > latest_date].copy()
        
        forecasts[commodity] = {
            'dates': [d.strftime('%Y-%m-%d') for d in future_data['ds']],
            'yhat': [round(v, 0) for v in future_data['yhat']],
            'yhat_lower': [round(v, 0) for v in future_data['yhat_lower']],
            'yhat_upper': [round(v, 0) for v in future_data['yhat_upper']],
        }
        
        # Future Anomaly Detection: Detect spikes > 15% from current price within 3 months
        current_price = latest_prices.get(commodity, 0)
        if current_price > 0:
            for _, row in future_data.iterrows():
                spike_pct = (row['yhat'] - current_price) / current_price * 100
                if spike_pct > 15:
                    future_anomalies.append({
                        'date': row['ds'].strftime('%Y-%m-%d'),
                        'commodity': commodity,
                        'shortName': SHORT_NAMES[commodity],
                        'category': CATEGORY_MAP[commodity],
                        'price': round(row['yhat'], 0),
                        'current_price': round(current_price, 0),
                        'spike_pct': round(spike_pct, 1),
                        'severity': 'prediction',
                        'action': 'Siapkan stok cadangan / pantau kuota distribusi'
                    })
                    break # just one alert per commodity is enough for future spike
    except Exception as e:
        print(f'  Warning: Failed to forecast {commodity}: {e}')

# ── 9. Monthly Category Prices (for stacked area) ───────────────
print('Computing category monthly prices...')
cat_monthly = df_clean.groupby([df_clean['date'].dt.to_period('M'), 'category'])['price'].mean().unstack()
cat_monthly.index = cat_monthly.index.to_timestamp()

category_monthly = {
    'dates': [d.strftime('%Y-%m-%d') for d in cat_monthly.index],
    'categories': {},
}
for cat in cat_monthly.columns:
    category_monthly['categories'][cat] = [
        round(v, 0) if not pd.isna(v) else 0 for v in cat_monthly[cat].values
    ]

# ── 9. KPI Summary ──────────────────────────────────────────────
print('Computing KPIs...')
n_critical = len([c for c in commodity_cards if c['status'] == 'critical'])
n_warning = len([c for c in commodity_cards if c['status'] == 'warning'])
avg_total_change = round(float(total_change.mean()), 1)
recent_anomaly_total = len([a for a in anomalies if a['date'] >= recent_start.strftime('%Y-%m-%d')])

kpi = {
    'totalCommodities': len(commodities),
    'criticalAlerts': n_critical,
    'warningAlerts': n_warning,
    'avgPriceChange': avg_total_change,
    'dataStartDate': df_clean['date'].min().strftime('%Y-%m-%d'),
    'dataEndDate': df_clean['date'].max().strftime('%Y-%m-%d'),
    'totalDataPoints': len(df_clean),
    'recentAnomalies': recent_anomaly_total,
}

# ── 10. Alert Feed (simulated recent alerts) ────────────────────
print('Generating alert feed...')
# Take most recent anomalies as alerts
alert_feed = []
for a in anomalies[:50]:  # top 50 most recent
    if a['severity'] == 'critical':
        action = 'Segera lakukan operasi pasar / inspeksi rantai pasok'
    else:
        action = 'Monitor harga harian, siapkan rencana intervensi'

    alert_feed.append({
        **a,
        'action': action,
    })

# Add future anomalies to the alert feed
future_anomalies.sort(key=lambda x: x['date'])
alert_feed = future_anomalies + alert_feed # Predictions go first

# ── 11. AI Executive Summary (Azure OpenAI) ─────────────────────
print('Generating AI Executive Summary...')

def build_anomaly_context(hist_anomalies, pred_anomalies):
    """Build a context string from anomalies for the LLM."""
    lines = []
    lines.append("=== ANOMALI HISTORIS TERBARU ===")
    for a in hist_anomalies[:5]:
        lines.append(
            f"- {a['shortName']}: Harga {a['price']:,.0f}, "
            f"deviasi {a['deviation_pct']:+.1f}% dari MA30, "
            f"severity: {a['severity']}, tanggal: {a['date']}"
        )
    if pred_anomalies:
        lines.append("\n=== PREDIKSI ANOMALI 90 HARI KE DEPAN ===")
        for a in pred_anomalies[:5]:
            lines.append(
                f"- {a['shortName']}: Prediksi harga {a['price']:,.0f} "
                f"(naik {a['spike_pct']:+.1f}% dari harga saat ini {a['current_price']:,.0f}), "
                f"tanggal: {a['date']}"
            )
    return "\n".join(lines)

def generate_fallback_insight(hist_anomalies, pred_anomalies, kpi_data):
    """Generate a rich, data-driven executive summary when Azure OpenAI is unavailable."""
    critical_items = [a for a in hist_anomalies[:20] if a['severity'] == 'critical']
    warning_items = [a for a in hist_anomalies[:20] if a['severity'] == 'warning']
    top_critical = critical_items[:3] if critical_items else hist_anomalies[:3]
    
    # Get unique critical commodity names with their worst deviation
    critical_details = {}
    for a in critical_items[:10]:
        name = a['shortName']
        if name not in critical_details or abs(a['deviation_pct']) > abs(critical_details[name]['deviation_pct']):
            critical_details[name] = a
    
    # Build detailed critical commodity descriptions
    critical_desc_parts = []
    for name, a in list(critical_details.items())[:3]:
        critical_desc_parts.append(
            f"{name} (lonjakan {a['deviation_pct']:+.1f}% pada {a['date']}, "
            f"harga Rp {a['price']:,.0f} vs rata-rata Rp {a['ma30']:,.0f})"
        )
    critical_desc = "; ".join(critical_desc_parts) if critical_desc_parts else "tidak ada"
    
    # Build prediction section
    pred_section = ""
    if pred_anomalies:
        pred_details = []
        for a in pred_anomalies[:3]:
            pred_details.append(
                f"{a['shortName']} (diprediksi naik {a['spike_pct']:+.1f}% "
                f"menjadi Rp {a['price']:,.0f} dari harga saat ini Rp {a['current_price']:,.0f})"
            )
        pred_desc = "; ".join(pred_details)
        pred_section = (
            f"\n\n📈 PREDIKSI 90 HARI KE DEPAN: Model machine learning Prophet mendeteksi "
            f"potensi lonjakan signifikan pada {len(pred_anomalies)} komoditas, terutama: {pred_desc}. "
            f"Kenaikan ini mengindikasikan tekanan inflasi struktural yang perlu diantisipasi "
            f"melalui mekanisme stabilisasi harga preventif."
        )
    
    # Build recommendation section
    rec_section = (
        f"\n\n💡 REKOMENDASI STRATEGIS: (1) Prioritaskan operasi pasar untuk komoditas berstatus KRITIS, "
        f"khususnya kelompok hortikultura yang memiliki volatilitas tertinggi; "
        f"(2) Koordinasi dengan Dinas Perindustrian dan Perdagangan Provinsi Aceh untuk "
        f"memastikan kelancaran rantai distribusi dari produsen ke pasar tradisional; "
        f"(3) Aktifkan mekanisme cadangan pangan daerah (buffer stock) untuk komoditas "
        f"yang diprediksi mengalami lonjakan dalam 90 hari ke depan."
    )
    
    return (
        f"🔍 RINGKASAN EKSEKUTIF — Sistem Aceh Resilience Monitor telah menganalisis "
        f"{kpi_data['totalDataPoints']:,} titik data harga harian dari "
        f"{kpi_data['totalCommodities']} komoditas pangan strategis "
        f"(periode {kpi_data['dataStartDate']} s/d {kpi_data['dataEndDate']}). "
        f"Dalam 90 hari terakhir, terdeteksi {kpi_data['recentAnomalies']} kejadian "
        f"anomali harga yang melampaui ambang batas statistik (>2σ dari rata-rata bergerak 30 hari). "
        f"Saat ini terdapat {kpi_data['criticalAlerts']} komoditas berstatus KRITIS dan "
        f"{kpi_data['warningAlerts']} komoditas berstatus WASPADA."
        f"\n\n⚠️ KOMODITAS KRITIS: {critical_desc}."
        f"{pred_section}"
        f"{rec_section}"
    )

# Attempt Azure OpenAI call
ai_insight = ""
AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT', '')
AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY', '')
AZURE_OPENAI_DEPLOYMENT = os.environ.get('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o-mini')

context_string = build_anomaly_context(anomalies, future_anomalies)

if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY:
    try:
        from openai import AzureOpenAI
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version="2024-06-01"
        )
        
        system_prompt = (
            "Anda adalah analis ekonomi senior pemerintah Provinsi Aceh. "
            "Berdasarkan data anomali harga pangan berikut dari sistem AI kami, "
            "buatkan ringkasan eksekutif 1 paragraf (maksimal 150 kata) untuk Gubernur. "
            "Sertakan: (1) komoditas mana yang paling kritis, "
            "(2) prediksi risiko 90 hari ke depan, "
            "(3) rekomendasi tindakan konkret. "
            "Gunakan bahasa formal namun mudah dipahami."
        )
        
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context_string}
            ],
            max_tokens=300,
            temperature=0.7
        )
        ai_insight = response.choices[0].message.content
        print('  ✅ AI Insight generated via Azure OpenAI')
    except Exception as e:
        print(f'  ⚠️ Azure OpenAI call failed: {e}')
        ai_insight = generate_fallback_insight(anomalies, future_anomalies, kpi)
        print('  ℹ️ Using fallback insight (data-driven summary)')
else:
    ai_insight = generate_fallback_insight(anomalies, future_anomalies, kpi)
    print('  ℹ️ Azure OpenAI keys not set. Using fallback insight (data-driven summary)')

# ── Assemble & Save ─────────────────────────────────────────────
dashboard_data = {
    'kpi': kpi,
    'commodityCards': commodity_cards,
    'timeseries': timeseries,
    'timeseriesRecentDaily': timeseries_daily_recent,
    'anomalies': anomalies[:200],  # cap for performance
    'alertFeed': alert_feed,
    'yoyData': yoy_data,
    'seasonality': seasonality_data,
    'volatility': volatility_data,
    'correlation': correlation_data,
    'categoryMonthly': category_monthly,
    'forecasts': forecasts,
    'categories': list(sorted(set(CATEGORY_MAP.values()))),
    'categoryIcons': CATEGORY_ICONS,
    'aiInsight': ai_insight,
}

os.makedirs(DASHBOARD_DIR, exist_ok=True)
output_path = DASHBOARD_DIR / 'dashboard_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=None)

# Also generate the embedded JS version (for file:// CORS compatibility)
output_js_path = DASHBOARD_DIR / 'dashboard_data.js'
with open(output_js_path, 'w', encoding='utf-8') as f:
    f.write('const DASHBOARD_DATA = ')
    json.dump(dashboard_data, f, ensure_ascii=False, indent=None)
    f.write(';')

file_size = os.path.getsize(output_path) / 1024
print(f'\n✅ Dashboard data saved to {output_path} ({file_size:.0f} KB)')
print(f'   Also generated: {output_js_path}')
print(f'   KPIs: {kpi}')
print(f'   Commodities: {len(commodities)}')
print(f'   Anomalies: {len(anomalies)}')
print(f'   Alerts: {len(alert_feed)}')
