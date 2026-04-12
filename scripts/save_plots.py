"""
Generate and save all EDA plots from the commodity price dataset.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings, os

warnings.filterwarnings('ignore')

PLOT_DIR = 'plots'
os.makedirs(PLOT_DIR, exist_ok=True)

sns.set_theme(style='whitegrid', palette='husl', font_scale=1.1)
plt.rcParams.update({
    'figure.figsize': (16, 6),
    'figure.dpi': 150,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
})

CATEGORY_COLORS = {
    'Beras': '#4E79A7', 'Daging Ayam': '#F28E2B', 'Daging Sapi': '#E15759',
    'Telur Ayam': '#76B7B2', 'Bawang Merah': '#59A14F', 'Bawang Putih': '#EDC948',
    'Cabai Merah': '#B07AA1', 'Cabai Rawit': '#FF9DA7', 'Minyak Goreng': '#9C755F',
    'Gula Pasir': '#BAB0AC',
}

CATEGORY_MAP = {
    'Beras Kualitas Bawah I': 'Beras', 'Beras Kualitas Bawah II': 'Beras',
    'Beras Kualitas Medium I': 'Beras', 'Beras Kualitas Medium II': 'Beras',
    'Beras Kualitas Super I': 'Beras', 'Beras Kualitas Super II': 'Beras',
    'Daging Ayam Ras Segar': 'Daging Ayam', 'Daging Sapi Kualitas 1': 'Daging Sapi',
    'Telur Ayam Ras Segar': 'Telur Ayam', 'Bawang Merah Ukuran Sedang': 'Bawang Merah',
    'Bawang Putih Ukuran Sedang': 'Bawang Putih', 'Cabai Merah Keriting': 'Cabai Merah',
    'Cabai Rawit Hijau': 'Cabai Rawit', 'Minyak Goreng Curah': 'Minyak Goreng',
    'Minyak Goreng Kemasan Bermerk 1': 'Minyak Goreng',
    'Minyak Goreng Kemasan Bermerk 2': 'Minyak Goreng',
    'Gula Pasir Kualitas Premium': 'Gula Pasir', 'Gula Pasir Lokal': 'Gula Pasir',
}

# ── Load Data ──────────────────────────────────────────────
def load_and_clean(filepath, year):
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
            if pd.isna(price) or price_str == '' or price_str == '-':
                price_val = np.nan
            else:
                price_val = float(price_str.replace(',', ''))
            records.append({'date': date, 'commodity': commodity_name, 'price': price_val, 'year': year})
    return pd.DataFrame(records)

print('Loading data...')
df = pd.concat([load_and_clean(f'{y}.xlsx', y) for y in [2023, 2024, 2025]], ignore_index=True)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['category'] = df['commodity'].map(CATEGORY_MAP)
df_clean = df.dropna(subset=['price']).copy()
print(f'Loaded {len(df_clean):,} clean records')

month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# ── PLOT 1: Box plots ──────────────────────────────────────
print('Plot 1: Box plots...')
commodities_sorted = df_clean.groupby('commodity')['price'].mean().sort_values(ascending=False).index
fig, axes = plt.subplots(2, 1, figsize=(18, 14))
high_price = [c for c in commodities_sorted if df_clean[df_clean['commodity']==c]['price'].mean() >= 25000]
low_price = [c for c in commodities_sorted if df_clean[df_clean['commodity']==c]['price'].mean() < 25000]
for ax, group, title in zip(axes, [high_price, low_price],
    ['High-Price Commodities (Mean >= Rp 25,000)', 'Low-Price Commodities (Mean < Rp 25,000)']):
    subset = df_clean[df_clean['commodity'].isin(group)]
    order = [c for c in commodities_sorted if c in group]
    sns.boxplot(data=subset, x='commodity', y='price', hue='year', order=order, ax=ax, palette='Set2', fliersize=2)
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.set_xlabel('')
    ax.set_ylabel('Price (Rp)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.tick_params(axis='x', rotation=35)
    ax.legend(title='Year', loc='upper right')
plt.suptitle('Price Distributions by Commodity & Year', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/01_boxplots.png', bbox_inches='tight')
plt.close()

# ── PLOT 2: Violin plots ──────────────────────────────────
print('Plot 2: Violin plots...')
volatile_commodities = ['Cabai Merah Keriting', 'Cabai Rawit Hijau', 'Bawang Merah Ukuran Sedang', 'Daging Ayam Ras Segar']
fig, axes = plt.subplots(1, 4, figsize=(20, 6), sharey=False)
for ax, commodity in zip(axes, volatile_commodities):
    subset = df_clean[df_clean['commodity'] == commodity]
    sns.violinplot(data=subset, x='year', y='price', ax=ax, palette='mako', inner='box', cut=0)
    ax.set_title(commodity, fontweight='bold', fontsize=11)
    ax.set_xlabel('Year')
    ax.set_ylabel('Price (Rp)' if ax == axes[0] else '')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
plt.suptitle('Price Distribution of Most Volatile Commodities', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/02_violin_volatile.png', bbox_inches='tight')
plt.close()

# ── PLOT 3: Time series by category ───────────────────────
print('Plot 3: Time series by category...')
categories = sorted(df_clean['category'].unique())
n_cats = len(categories)
fig, axes = plt.subplots(n_cats, 1, figsize=(18, 3.5 * n_cats), sharex=True)
for ax, cat in zip(axes, categories):
    cat_df = df_clean[df_clean['category'] == cat]
    color = CATEGORY_COLORS.get(cat, '#333333')
    for commodity in cat_df['commodity'].unique():
        cdf = cat_df[cat_df['commodity'] == commodity].sort_values('date')
        ax.plot(cdf['date'], cdf['price'], label=commodity, linewidth=0.8, alpha=0.85)
    ax.set_title(f'{cat}', fontweight='bold', fontsize=13, loc='left', color=color)
    ax.set_ylabel('Price (Rp)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.legend(loc='upper left', fontsize=8, ncol=3)
    ax.grid(True, alpha=0.3)
    for yr in [2024, 2025]:
        ax.axvline(pd.Timestamp(f'{yr}-01-01'), color='gray', linestyle='--', alpha=0.5)
axes[-1].set_xlabel('Date')
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.suptitle('Daily Commodity Prices (2023-2025)', fontsize=18, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/03_timeseries_all.png', bbox_inches='tight')
plt.close()

# ── PLOT 4: Volatile commodities + MA ─────────────────────
print('Plot 4: Volatile + MA...')
highlight = ['Cabai Merah Keriting', 'Cabai Rawit Hijau', 'Bawang Merah Ukuran Sedang']
fig, axes = plt.subplots(len(highlight), 1, figsize=(18, 4 * len(highlight)), sharex=True)
for ax, commodity in zip(axes, highlight):
    cdf = df_clean[df_clean['commodity'] == commodity].sort_values('date')
    ax.fill_between(cdf['date'], cdf['price'], alpha=0.15, color='#E15759')
    ax.plot(cdf['date'], cdf['price'], linewidth=0.6, alpha=0.5, color='#E15759', label='Daily')
    ma30 = cdf.set_index('date')['price'].rolling('30D').mean()
    ax.plot(ma30.index, ma30.values, linewidth=2, color='#4E79A7', label='30-day MA')
    ax.set_title(commodity, fontweight='bold', fontsize=13)
    ax.set_ylabel('Price (Rp)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    for yr in [2024, 2025]:
        ax.axvline(pd.Timestamp(f'{yr}-01-01'), color='gray', linestyle='--', alpha=0.5)
plt.suptitle('Volatile Commodities - Daily Prices with 30-Day Moving Average', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/04_volatile_ma30.png', bbox_inches='tight')
plt.close()

# ── PLOT 5: Total price change bar ────────────────────────
print('Plot 5: Total price change...')
yearly_mean = df_clean.groupby(['year', 'commodity'])['price'].mean().unstack(level=0)
total_change = ((yearly_mean[2025] - yearly_mean[2023]) / yearly_mean[2023] * 100).sort_values()
fig, ax = plt.subplots(figsize=(12, 10))
colors = ['#E15759' if v > 20 else '#F28E2B' if v > 10 else '#59A14F' if v >= 0 else '#4E79A7' for v in total_change.values]
bars = ax.barh(range(len(total_change)), total_change.values, color=colors, edgecolor='white', height=0.7)
ax.set_yticks(range(len(total_change)))
ax.set_yticklabels(total_change.index)
for bar, val in zip(bars, total_change.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{val:+.1f}%', va='center', fontsize=10, fontweight='bold')
ax.set_xlabel('Total Price Change (%)', fontsize=12)
ax.set_title('Total Price Change 2023 to 2025 by Commodity', fontsize=15, fontweight='bold')
ax.axvline(0, color='black', linewidth=0.8)
ax.axvline(20, color='red', linewidth=0.8, linestyle='--', alpha=0.5, label='> 20% threshold')
ax.legend()
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/05_total_change_bar.png', bbox_inches='tight')
plt.close()

# ── PLOT 6: YoY grouped bar ──────────────────────────────
print('Plot 6: YoY grouped bar...')
change_23_24 = ((yearly_mean[2024] - yearly_mean[2023]) / yearly_mean[2023] * 100)
change_24_25 = ((yearly_mean[2025] - yearly_mean[2024]) / yearly_mean[2024] * 100)
commodities_order = total_change.sort_values(ascending=False).index
x = np.arange(len(commodities_order))
width = 0.35
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(x - width/2, change_23_24[commodities_order], width, label='2023-2024', color='#4E79A7', alpha=0.85)
ax.bar(x + width/2, change_24_25[commodities_order], width, label='2024-2025', color='#E15759', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(commodities_order, rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Price Change (%)')
ax.set_title('Year-over-Year Price Changes by Commodity', fontsize=15, fontweight='bold')
ax.axhline(0, color='black', linewidth=0.8)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/06_yoy_comparison.png', bbox_inches='tight')
plt.close()

# ── PLOT 7: CV heatmap ────────────────────────────────────
print('Plot 7: CV heatmap...')
cv_for_heatmap = df_clean.groupby(['year', 'commodity'])['price'].agg(lambda x: x.std() / x.mean() * 100).unstack(level=0).round(2)
cv_for_heatmap = cv_for_heatmap.loc[cv_for_heatmap.mean(axis=1).sort_values(ascending=False).index]
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(cv_for_heatmap, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=0.5, ax=ax, cbar_kws={'label': 'CV (%)'})
ax.set_title('Price Volatility (CV %) by Commodity & Year', fontsize=14, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/07_cv_heatmap.png', bbox_inches='tight')
plt.close()

# ── PLOT 8: Correlation heatmap ───────────────────────────
print('Plot 8: Correlation heatmap...')
price_wide = df_clean.pivot_table(index='date', columns='commodity', values='price')
price_wide.columns.name = None
corr = price_wide.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
fig, ax = plt.subplots(figsize=(16, 14))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            linewidths=0.5, ax=ax, annot_kws={'size': 8}, cbar_kws={'label': 'Pearson Correlation'})
ax.set_title('Price Correlation Matrix (2023-2025)', fontsize=15, fontweight='bold')
ax.tick_params(axis='both', labelsize=9)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/08_correlation_matrix.png', bbox_inches='tight')
plt.close()

# ── PLOT 9: Monthly seasonality ───────────────────────────
print('Plot 9: Monthly seasonality...')
monthly_avg = df_clean.groupby(['month', 'commodity'])['price'].mean().reset_index()
seasonal_commodities = ['Cabai Merah Keriting', 'Cabai Rawit Hijau', 'Bawang Merah Ukuran Sedang',
                        'Daging Ayam Ras Segar', 'Telur Ayam Ras Segar', 'Bawang Putih Ukuran Sedang']
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
for ax, commodity in zip(axes.flat, seasonal_commodities):
    for year in [2023, 2024, 2025]:
        yr_data = df_clean[(df_clean['commodity'] == commodity) & (df_clean['year'] == year)]
        monthly = yr_data.groupby('month')['price'].mean()
        ax.plot(monthly.index, monthly.values, marker='o', markersize=4, label=str(year), linewidth=1.5)
    overall = monthly_avg[monthly_avg['commodity'] == commodity]
    ax.plot(overall['month'], overall['price'], '--', color='black', alpha=0.5, linewidth=2, label='3-yr Avg')
    ax.set_title(commodity, fontweight='bold', fontsize=11)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}K'))
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
plt.suptitle('Monthly Seasonality Patterns by Commodity', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/09_seasonality.png', bbox_inches='tight')
plt.close()

# ── PLOT 10: Monthly Z-score heatmap ─────────────────────
print('Plot 10: Z-score heatmap...')
monthly_pivot = df_clean.groupby(['commodity', 'month'])['price'].mean().unstack()
monthly_normalized = monthly_pivot.apply(lambda x: (x - x.mean()) / x.std(), axis=1)
fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(monthly_normalized, annot=True, fmt='.2f', cmap='RdYlGn_r', center=0, linewidths=0.5, ax=ax,
            xticklabels=month_labels, cbar_kws={'label': 'Z-Score (higher = more expensive)'})
ax.set_title('Monthly Price Seasonality Heatmap (Z-Score Normalized)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/10_zscore_heatmap.png', bbox_inches='tight')
plt.close()

# ── PLOT 11: Daily returns distribution ───────────────────
print('Plot 11: Daily returns distribution...')
price_wide_sorted = price_wide.sort_index()
daily_returns = price_wide_sorted.pct_change() * 100
returns_stats = daily_returns.describe().T[['mean', 'std', 'min', 'max']].round(3)
returns_stats.columns = ['Mean Return (%)', 'Std Return (%)', 'Max Drop (%)', 'Max Gain (%)']
returns_stats = returns_stats.sort_values('Std Return (%)', ascending=False)
top_volatile = returns_stats.head(6).index.tolist()
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
for ax, commodity in zip(axes.flat, top_volatile):
    data = daily_returns[commodity].dropna()
    ax.hist(data, bins=50, color='#4E79A7', alpha=0.7, edgecolor='white', density=True)
    kde_x = np.linspace(data.min(), data.max(), 200)
    kde = stats.gaussian_kde(data)
    ax.plot(kde_x, kde(kde_x), color='#E15759', linewidth=2)
    ax.axvline(0, color='black', linestyle='--', alpha=0.5)
    ax.set_title(commodity, fontweight='bold', fontsize=11)
    ax.set_xlabel('Daily Return (%)')
    ax.set_ylabel('Density' if ax in axes[:, 0] else '')
    mu, sigma = data.mean(), data.std()
    ax.text(0.95, 0.95, f'mu={mu:.3f}%\nsigma={sigma:.2f}%', transform=ax.transAxes, va='top', ha='right',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
plt.suptitle('Distribution of Daily Price Changes - Most Volatile Commodities', fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/11_daily_returns.png', bbox_inches='tight')
plt.close()

# ── PLOT 12: Category bar chart ───────────────────────────
print('Plot 12: Category bar chart...')
cat_yearly = df_clean.groupby(['year', 'category'])['price'].mean().unstack(level=0).round(0)
fig, ax = plt.subplots(figsize=(14, 8))
cat_order = cat_yearly.mean(axis=1).sort_values(ascending=True).index
x = np.arange(len(cat_order))
width = 0.25
for i, year in enumerate([2023, 2024, 2025]):
    values = cat_yearly.loc[cat_order, year]
    ax.barh(x + i * width, values, width, label=str(year), alpha=0.85)
ax.set_yticks(x + width)
ax.set_yticklabels(cat_order)
ax.set_xlabel('Average Price (Rp)')
ax.set_title('Average Price by Category & Year', fontsize=15, fontweight='bold')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.legend(title='Year')
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/12_category_prices.png', bbox_inches='tight')
plt.close()

# ── PLOT 13: Stacked area chart ───────────────────────────
print('Plot 13: Stacked area chart...')
cat_monthly = df_clean.groupby([df_clean['date'].dt.to_period('M'), 'category'])['price'].mean().unstack()
cat_monthly.index = cat_monthly.index.to_timestamp()
fig, ax = plt.subplots(figsize=(18, 8))
cols_to_plot = [c for c in cat_monthly.columns if c != 'Daging Sapi']
colors_list = [CATEGORY_COLORS.get(c, '#333') for c in cols_to_plot]
ax.stackplot(cat_monthly.index, [cat_monthly[c] for c in cols_to_plot], labels=cols_to_plot, colors=colors_list, alpha=0.8)
ax.set_title('Monthly Average Prices by Category (Stacked, excl. Daging Sapi)', fontsize=14, fontweight='bold')
ax.set_ylabel('Combined Price (Rp)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.legend(loc='upper left', fontsize=9, ncol=3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.grid(True, alpha=0.3)
for yr in [2024, 2025]:
    ax.axvline(pd.Timestamp(f'{yr}-01-01'), color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(f'{PLOT_DIR}/13_stacked_area.png', bbox_inches='tight')
plt.close()

print(f'\n✅ All 13 plots saved to {PLOT_DIR}/')
