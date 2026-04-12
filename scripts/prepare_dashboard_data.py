"""
Prepare dashboard data from Excel commodity price files.
Outputs dashboard/dashboard_data.json for the ARM web dashboard.
"""
import pandas as pd
import numpy as np
import json
import os

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
df = pd.concat([load_and_clean(f'{y}.xlsx', y) for y in [2023, 2024, 2025]], ignore_index=True)
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

# ── 8. Monthly Category Prices (for stacked area) ───────────────
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
    'categories': list(sorted(set(CATEGORY_MAP.values()))),
    'categoryIcons': CATEGORY_ICONS,
}

os.makedirs('dashboard', exist_ok=True)
output_path = 'dashboard/dashboard_data.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=None)

file_size = os.path.getsize(output_path) / 1024
print(f'\n✅ Dashboard data saved to {output_path} ({file_size:.0f} KB)')
print(f'   KPIs: {kpi}')
print(f'   Commodities: {len(commodities)}')
print(f'   Anomalies: {len(anomalies)}')
print(f'   Alerts: {len(alert_feed)}')
