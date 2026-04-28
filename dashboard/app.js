/**
 * Aceh Resilience Monitor (ARM) — Dashboard Application
 * Interactive commodity price monitoring & anomaly detection
 */

// ── Globals ──────────────────────────────────────────────────────
let DATA = null;
let charts = {};
let selectedCommodity = null;
let activeCategory = 'all';
let showForecast = false;

// ── Color Palettes ───────────────────────────────────────────────
const CATEGORY_COLORS = {
  'Beras': '#4E79A7',
  'Daging Ayam': '#F28E2B',
  'Daging Sapi': '#E15759',
  'Telur Ayam': '#76B7B2',
  'Bawang Merah': '#59A14F',
  'Bawang Putih': '#EDC948',
  'Cabai Merah': '#B07AA1',
  'Cabai Rawit': '#FF9DA7',
  'Minyak Goreng': '#9C755F',
  'Gula Pasir': '#BAB0AC',
};

const STATUS_COLORS = {
  normal: '#22c55e',
  warning: '#f59e0b',
  critical: '#ef4444',
  prediction: '#a855f7', // Purple for forecasts
};

const MONTH_LABELS = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];

// ── Utility Functions ────────────────────────────────────────────
function formatPrice(val) {
  if (val == null) return '-';
  return 'Rp ' + Math.round(val).toLocaleString('id-ID');
}

function formatPriceShort(val) {
  if (val >= 1000) return (val / 1000).toFixed(0) + 'K';
  return val.toFixed(0);
}

function formatChange(val) {
  const sign = val > 0 ? '+' : '';
  return sign + val.toFixed(1) + '%';
}

function getChangeClass(val) {
  if (val > 5) return 'positive';
  if (val < -5) return 'negative';
  return 'neutral';
}

function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ── Load Data ────────────────────────────────────────────────────
async function loadData() {
  try {
    // Use embedded data (dashboard_data.js) to avoid CORS issues with file://
    if (typeof DASHBOARD_DATA !== 'undefined') {
      DATA = DASHBOARD_DATA;
      return true;
    }
    // Fallback to fetch if served via HTTP
    const resp = await fetch('dashboard_data.json');
    DATA = await resp.json();
    return true;
  } catch (e) {
    console.error('Failed to load data:', e);
    return false;
  }
}

// ── Initialize App ───────────────────────────────────────────────
async function initApp() {
  const loaded = await loadData();
  if (!loaded) {
    document.getElementById('loading-text').textContent = 'Gagal memuat data!';
    return;
  }

  renderKPIs();
  renderAIInsight();
  renderCommodityGrid();
  renderPriceTrendChart();
  renderYoYChart();
  renderSeasonalityHeatmap();
  renderVolatilityHeatmap();
  renderAlertFeed();
  renderAnomalyTable();
  renderCategoryAreaChart();

  // Update date display
  document.getElementById('data-date-range').textContent =
    `${DATA.kpi.dataStartDate} — ${DATA.kpi.dataEndDate}`;

  // Hide loading
  await delay(400);
  document.getElementById('loading-overlay').classList.add('hidden');
}

// ── Render KPIs ──────────────────────────────────────────────────
function renderKPIs() {
  const k = DATA.kpi;
  const grid = document.getElementById('kpi-grid');
  const kpis = [
    {
      label: 'Total Komoditas Dipantau',
      value: k.totalCommodities,
      color: 'teal',
      detail: '18 komoditas pangan strategis',
    },
    {
      label: 'Status Kritis',
      value: k.criticalAlerts,
      color: 'red',
      detail: 'Komoditas dengan volatilitas/kenaikan tinggi',
    },
    {
      label: 'Status Waspada',
      value: k.warningAlerts,
      color: 'yellow',
      detail: 'Komoditas perlu perhatian',
    },
    {
      label: 'Rata-rata Kenaikan (3 Thn)',
      value: formatChange(k.avgPriceChange),
      color: k.avgPriceChange > 15 ? 'red' : 'blue',
      detail: '2023 → 2025 seluruh komoditas',
    },
    {
      label: 'Anomali (90 Hari Terakhir)',
      value: k.recentAnomalies,
      color: 'purple',
      detail: 'Lonjakan harga di luar 2σ dari MA30',
    },
    {
      label: 'Total Data Point',
      value: k.totalDataPoints.toLocaleString('id-ID'),
      color: 'green',
      detail: `${k.dataStartDate} s/d ${k.dataEndDate}`,
    },
  ];

  grid.innerHTML = kpis.map(kpi => `
    <div class="kpi-card ${kpi.color}" id="kpi-${kpi.label.replace(/\s/g, '-')}">
      <div class="kpi-label">${kpi.label}</div>
      <div class="kpi-value ${kpi.color}">${kpi.value}</div>
      <div class="kpi-detail">${kpi.detail}</div>
    </div>
  `).join('');
}

// ── Render Commodity Status Grid ─────────────────────────────────
function renderCommodityGrid() {
  const grid = document.getElementById('commodity-grid');
  const cards = DATA.commodityCards;

  // Sort: critical first, then warning, then normal
  const order = { critical: 0, warning: 1, normal: 2 };
  const sorted = [...cards].sort((a, b) => order[a.status] - order[b.status]);

  grid.innerHTML = sorted.map(c => `
    <div class="commodity-card status-${c.status}" 
         data-commodity="${c.commodity}"
         onclick="selectCommodity('${c.commodity}')"
         id="card-${c.commodity.replace(/\s/g, '-')}">
      <div class="commodity-header">
        <span class="commodity-icon">${c.icon}</span>
        <span class="commodity-name">${c.shortName}</span>
      </div>
      <div class="commodity-price">${formatPrice(c.latestPrice)}</div>
      <div class="commodity-meta">
        <span class="commodity-change ${getChangeClass(c.totalChange)}">
          ${formatChange(c.totalChange)}
        </span>
        <span class="commodity-cv">CV ${c.cv2025}%</span>
      </div>
      <div class="mt-1">
        <span class="status-badge ${c.status}">
          ${c.status === 'critical' ? '🔴 Kritis' : c.status === 'warning' ? '🟡 Waspada' : '🟢 Aman'}
        </span>
        ${c.recentAnomalies > 0 ? `<span class="notif-count" style="margin-left:6px">${c.recentAnomalies}</span>` : ''}
      </div>
    </div>
  `).join('');
}

// ── Select Commodity (drill-down) ────────────────────────────────
function selectCommodity(commodity) {
  // Toggle selection
  if (selectedCommodity === commodity) {
    selectedCommodity = null;
    document.querySelectorAll('.commodity-card').forEach(c => c.classList.remove('selected'));
    document.getElementById('detail-panel').classList.remove('active');
    updatePriceTrendChart();
    return;
  }

  selectedCommodity = commodity;

  // Highlight card
  document.querySelectorAll('.commodity-card').forEach(c => {
    c.classList.toggle('selected', c.dataset.commodity === commodity);
  });

  // Show detail panel
  showCommodityDetail(commodity);

  // Update price chart to show only this commodity
  updatePriceTrendChart(commodity);

  // Scroll to detail
  document.getElementById('detail-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showCommodityDetail(commodity) {
  const panel = document.getElementById('detail-panel');
  const card = DATA.commodityCards.find(c => c.commodity === commodity);
  const ts = DATA.timeseries[commodity];
  const vol = DATA.volatility[commodity];
  const anomalies = DATA.anomalies.filter(a => a.commodity === commodity).slice(0, 15);

  panel.classList.add('active');
  panel.innerHTML = `
    <div class="glass-card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
        <div>
          <h3 style="font-size:18px;font-weight:700">${card.icon} ${commodity}</h3>
          <span class="text-muted text-sm">Kategori: ${card.category} | Status: 
            <span class="status-badge ${card.status}">${card.status === 'critical' ? '🔴 Kritis' : card.status === 'warning' ? '🟡 Waspada' : '🟢 Aman'}</span>
          </span>
        </div>
        <button class="chart-btn" onclick="selectCommodity('${commodity}')">✕ Tutup</button>
      </div>
      <div class="kpi-grid" style="grid-template-columns:repeat(4,1fr)">
        <div class="kpi-card teal">
          <div class="kpi-label">Harga Terakhir</div>
          <div class="kpi-value teal" style="font-size:20px">${formatPrice(card.latestPrice)}</div>
        </div>
        <div class="kpi-card ${card.totalChange > 20 ? 'red' : 'blue'}">
          <div class="kpi-label">Perubahan 3 Tahun</div>
          <div class="kpi-value ${card.totalChange > 20 ? 'red' : 'blue'}" style="font-size:20px">${formatChange(card.totalChange)}</div>
        </div>
        <div class="kpi-card ${card.cv2025 > 15 ? 'red' : 'yellow'}">
          <div class="kpi-label">Volatilitas 2025 (CV)</div>
          <div class="kpi-value ${card.cv2025 > 15 ? 'red' : 'yellow'}" style="font-size:20px">${card.cv2025}%</div>
        </div>
        <div class="kpi-card purple">
          <div class="kpi-label">Anomali (90 Hari)</div>
          <div class="kpi-value purple" style="font-size:20px">${card.recentAnomalies}</div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px" class="mt-2">
        <div>
          <h4 class="mb-1">📊 Volatilitas Per Tahun</h4>
          <div class="stat-row"><span class="stat-label">2023</span><span class="stat-value">${vol['2023']}%</span></div>
          <div class="stat-row"><span class="stat-label">2024</span><span class="stat-value">${vol['2024']}%</span></div>
          <div class="stat-row"><span class="stat-label">2025</span><span class="stat-value">${vol['2025']}%</span></div>
        </div>
        <div>
          <h4 class="mb-1">⚠️ Anomali Terdeteksi</h4>
          ${anomalies.length === 0 ? '<p class="text-muted text-sm">Tidak ada anomali terdeteksi</p>' :
            `<div style="max-height:180px;overflow-y:auto">
              ${anomalies.map(a => `
                <div class="stat-row">
                  <span class="stat-label">${a.date}</span>
                  <span class="anomaly-deviation ${a.deviation_pct > 0 ? 'positive' : 'negative'}">
                    ${formatChange(a.deviation_pct)} dari MA30
                  </span>
                </div>
              `).join('')}
            </div>`
          }
        </div>
      </div>
    </div>
  `;
}

// ── Price Trend Chart ────────────────────────────────────────────
function renderPriceTrendChart() {
  const ctx = document.getElementById('chart-price-trend').getContext('2d');

  // Category filter buttons
  const controls = document.getElementById('trend-category-filter');
  const categories = ['all', ...DATA.categories];
  controls.innerHTML = categories.map(cat => `
    <button class="chart-btn ${cat === 'all' ? 'active' : ''}" 
            onclick="filterTrendCategory('${cat}')"
            data-category="${cat}">
      ${cat === 'all' ? '🔍 Semua' : (DATA.categoryIcons[cat] || '') + ' ' + cat}
    </button>
  `).join('');

  charts.priceTrend = new Chart(ctx, {
    type: 'line',
    data: { datasets: [] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 11 },
            boxWidth: 12,
            padding: 12,
            usePointStyle: true,
          },
        },
        tooltip: {
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleColor: '#f1f5f9',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
          padding: 12,
          titleFont: { family: 'Inter', weight: '600' },
          bodyFont: { family: 'JetBrains Mono', size: 12 },
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${formatPrice(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'month',
            displayFormats: { month: 'MMM yy' },
          },
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#64748b', font: { size: 10 } },
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: {
            color: '#64748b',
            font: { size: 10 },
            callback: (v) => formatPriceShort(v),
          },
        },
      },
    },
  });

  updatePriceTrendChart();
}

function toggleForecast() {
  showForecast = !showForecast;
  const btn = document.getElementById('toggle-forecast-btn');
  btn.classList.toggle('active', showForecast);
  btn.innerHTML = showForecast ? '✨ Sembunyikan Prediksi' : '🔮 Tampilkan Prediksi 90 Hari';
  updatePriceTrendChart(selectedCommodity);
}

function updatePriceTrendChart(singleCommodity = null) {
  const ts = DATA.timeseries;
  const forecasts = DATA.forecasts || {};
  const datasets = [];

  for (const [commodity, data] of Object.entries(ts)) {
    if (singleCommodity && commodity !== singleCommodity) continue;
    if (!singleCommodity && activeCategory !== 'all' && data.category !== activeCategory) continue;

    const color = CATEGORY_COLORS[data.category] || '#94a3b8';
    
    // 1. Main historical data
    datasets.push({
      label: data.shortName,
      data: data.dates.map((d, i) => ({ x: d, y: data.prices[i] })),
      borderColor: color,
      backgroundColor: color + '15',
      borderWidth: singleCommodity ? 2.5 : 1.5,
      pointRadius: singleCommodity ? 2 : 0,
      pointHoverRadius: 4,
      fill: !!singleCommodity,
      tension: 0.3,
      order: 10
    });

    // 2. Forecast data (if enabled)
    if (showForecast && forecasts[commodity]) {
      const fc = forecasts[commodity];
      const lastHistDate = data.dates[data.dates.length - 1];
      const lastHistPrice = data.prices[data.prices.length - 1];

      // Add a bridge point from the last historical data to the first forecast
      const forecastPoints = [
        { x: lastHistDate, y: lastHistPrice },
        ...fc.dates.map((d, i) => ({ x: d, y: fc.yhat[i] }))
      ];

      datasets.push({
        label: `${data.shortName} (Prediksi)`,
        data: forecastPoints,
        borderColor: color,
        borderDash: [5, 5],
        borderWidth: 2,
        pointRadius: 0,
        fill: false,
        tension: 0.4,
        order: 5
      });

      // 3. Confidence Interval (Shaded Area)
      if (singleCommodity) {
        const lowerPoints = [
            { x: lastHistDate, y: lastHistPrice },
            ...fc.dates.map((d, i) => ({ x: d, y: fc.yhat_lower[i] }))
        ];
        const upperPoints = [
            { x: lastHistDate, y: lastHistPrice },
            ...fc.dates.map((d, i) => ({ x: d, y: fc.yhat_upper[i] }))
        ];

        datasets.push({
          label: `${data.shortName} (Batas Atas)`,
          data: upperPoints,
          borderColor: 'transparent',
          backgroundColor: color + '10',
          pointRadius: 0,
          fill: false,
          tension: 0.4,
          order: 20
        });

        datasets.push({
          label: `${data.shortName} (Batas Bawah)`,
          data: lowerPoints,
          borderColor: 'transparent',
          backgroundColor: color + '10',
          pointRadius: 0,
          fill: '-1', // Fill between this and the previous dataset (Upper)
          tension: 0.4,
          order: 21
        });
      }
    }
  }

  charts.priceTrend.data.datasets = datasets;
  charts.priceTrend.update('none');
}

function filterTrendCategory(category) {
  activeCategory = category;
  document.querySelectorAll('#trend-category-filter .chart-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.category === category);
  });
  if (selectedCommodity) {
    selectedCommodity = null;
    document.querySelectorAll('.commodity-card').forEach(c => c.classList.remove('selected'));
    document.getElementById('detail-panel').classList.remove('active');
  }
  updatePriceTrendChart();
}

// ── YoY Comparison Chart ─────────────────────────────────────────
function renderYoYChart() {
  const ctx = document.getElementById('chart-yoy').getContext('2d');
  const yoy = DATA.yoyData;
  const labels = yoy.map(y => y.shortName);

  charts.yoy = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: '2023 → 2024',
          data: yoy.map(y => y.change_23_24),
          backgroundColor: 'rgba(59, 130, 246, 0.7)',
          borderColor: 'rgba(59, 130, 246, 1)',
          borderWidth: 1,
          borderRadius: 4,
        },
        {
          label: '2024 → 2025',
          data: yoy.map(y => y.change_24_25),
          backgroundColor: 'rgba(239, 68, 68, 0.7)',
          borderColor: 'rgba(239, 68, 68, 1)',
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 11 },
            padding: 16,
            usePointStyle: true,
          },
        },
        tooltip: {
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleColor: '#f1f5f9',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw > 0 ? '+' : ''}${ctx.raw.toFixed(1)}%`,
          },
        },
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: {
            color: '#64748b',
            font: { size: 10 },
            callback: (v) => v + '%',
          },
        },
        y: {
          grid: { display: false },
          ticks: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 10 },
          },
        },
      },
    },
  });
}

// ── Seasonality Heatmap ──────────────────────────────────────────
function renderSeasonalityHeatmap() {
  const container = document.getElementById('seasonality-heatmap');
  const season = DATA.seasonality;
  const commodities = Object.keys(season);

  // Color scale: green (negative/cheap) → white (neutral) → red (expensive)
  function zScoreColor(z) {
    const clamped = Math.max(-3, Math.min(3, z));
    if (clamped >= 0) {
      const intensity = clamped / 3;
      const r = 239, g = Math.round(68 + (1 - intensity) * 187), b = Math.round(68 + (1 - intensity) * 187);
      return `rgba(${r}, ${g}, ${b}, ${0.2 + intensity * 0.6})`;
    } else {
      const intensity = Math.abs(clamped) / 3;
      const r = Math.round(34 + (1 - intensity) * 221), g = 197, b = Math.round(94 + (1 - intensity) * 161);
      return `rgba(${r}, ${g}, ${b}, ${0.2 + intensity * 0.6})`;
    }
  }

  function textColor(z) {
    return Math.abs(z) > 1.5 ? '#fff' : '#94a3b8';
  }

  let html = '<div class="heatmap-grid">';

  // Header row
  html += '<div class="heatmap-row">';
  html += '<div class="heatmap-label"></div>';
  MONTH_LABELS.forEach(m => {
    html += `<div class="heatmap-cell heatmap-header">${m}</div>`;
  });
  html += '</div>';

  // Data rows
  commodities.forEach(commodity => {
    const d = season[commodity];
    html += '<div class="heatmap-row">';
    html += `<div class="heatmap-label" title="${commodity}">${d.shortName}</div>`;
    d.values.forEach((v, i) => {
      const bg = zScoreColor(v);
      const tc = textColor(v);
      html += `<div class="heatmap-cell" style="background:${bg};color:${tc}" 
               title="${commodity} — ${MONTH_LABELS[i]}: Z=${v.toFixed(2)}">${v.toFixed(1)}</div>`;
    });
    html += '</div>';
  });

  html += '</div>';
  container.innerHTML = html;
}

// ── Volatility Heatmap ───────────────────────────────────────────
function renderVolatilityHeatmap() {
  const container = document.getElementById('volatility-heatmap');
  const vol = DATA.volatility;
  const commodities = Object.keys(vol);

  // Sort by 2025 CV descending
  commodities.sort((a, b) => (vol[b]['2025'] || 0) - (vol[a]['2025'] || 0));

  function cvColor(cv) {
    if (cv > 20) return { bg: 'rgba(239, 68, 68, 0.6)', text: '#fff' };
    if (cv > 10) return { bg: 'rgba(245, 158, 11, 0.5)', text: '#fff' };
    if (cv > 5) return { bg: 'rgba(245, 158, 11, 0.25)', text: '#fcd34d' };
    return { bg: 'rgba(34, 197, 94, 0.15)', text: '#86efac' };
  }

  let html = '<div class="heatmap-grid">';

  // Header row
  html += '<div class="heatmap-row">';
  html += '<div class="heatmap-label"></div>';
  ['2023', '2024', '2025'].forEach(y => {
    html += `<div class="heatmap-cell heatmap-header">${y}</div>`;
  });
  html += '</div>';

  commodities.forEach(commodity => {
    const d = vol[commodity];
    html += '<div class="heatmap-row">';
    html += `<div class="heatmap-label" title="${commodity}">${d.shortName}</div>`;
    ['2023', '2024', '2025'].forEach(y => {
      const v = d[y];
      const c = cvColor(v);
      html += `<div class="heatmap-cell" style="background:${c.bg};color:${c.text};min-width:80px"
               title="${commodity} ${y}: CV=${v}%">${v}%</div>`;
    });
    html += '</div>';
  });

  html += '</div>';
  container.innerHTML = html;
}

// ── Alert Feed ───────────────────────────────────────────────────
function renderAlertFeed() {
  const container = document.getElementById('alert-feed');
  const alerts = DATA.alertFeed.slice(0, 25);

  container.innerHTML = alerts.map((a, i) => `
    <div class="alert-item" style="animation-delay: ${i * 50}ms">
      <div class="alert-indicator ${a.severity}"></div>
      <div class="alert-content">
        <div class="alert-title">${a.shortName} — ${
          a.severity === 'critical' ? '🚨 KRITIS' : 
          a.severity === 'prediction' ? '🔮 PREDIKSI' : '⚠️ WASPADA'
        }</div>
        <div class="alert-detail">
          ${a.severity === 'prediction' 
            ? `Prediksi: ${formatPrice(a.price)} (Spike ${formatChange(a.spike_pct)})`
            : `Harga: ${formatPrice(a.price)} | MA30: ${formatPrice(a.ma30)} | Deviasi: ${formatChange(a.deviation_pct)}`
          }
        </div>
        <div class="alert-action">↳ ${a.action}</div>
      </div>
      <div class="alert-date">${a.date}</div>
    </div>
  `).join('');
}

// ── Anomaly Table ────────────────────────────────────────────────
function renderAnomalyTable() {
  const container = document.getElementById('anomaly-table-body');
  // Show most recent anomalies, limit to 50 for performance
  const anomalies = DATA.anomalies.slice(0, 50);

  container.innerHTML = anomalies.map(a => `
    <tr>
      <td class="font-mono">${a.date}</td>
      <td>${a.shortName}</td>
      <td>${a.category}</td>
      <td class="font-mono">${formatPrice(a.price)}</td>
      <td class="font-mono">${formatPrice(a.ma30)}</td>
      <td class="anomaly-deviation ${a.deviation_pct > 0 ? 'positive' : 'negative'}">
        ${formatChange(a.deviation_pct)}
      </td>
      <td class="font-mono">${a.z_score.toFixed(1)}σ</td>
      <td class="severity-cell ${a.severity}">${a.severity === 'critical' ? '🔴 Kritis' : '🟡 Waspada'}</td>
    </tr>
  `).join('');
}

// ── Category Stacked Area Chart ──────────────────────────────────
function renderCategoryAreaChart() {
  const ctx = document.getElementById('chart-category-area').getContext('2d');
  const cm = DATA.categoryMonthly;
  const categories = Object.keys(cm.categories).filter(c => c !== 'Daging Sapi'); // exclude outlier

  const datasets = categories.map(cat => ({
    label: cat,
    data: cm.categories[cat],
    backgroundColor: (CATEGORY_COLORS[cat] || '#666') + '80',
    borderColor: CATEGORY_COLORS[cat] || '#666',
    borderWidth: 1,
    fill: true,
    tension: 0.3,
    pointRadius: 0,
  }));

  charts.categoryArea = new Chart(ctx, {
    type: 'line',
    data: {
      labels: cm.dates,
      datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: '#94a3b8',
            font: { family: 'Inter', size: 10 },
            boxWidth: 10,
            padding: 10,
            usePointStyle: true,
          },
        },
        tooltip: {
          mode: 'index',
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleColor: '#f1f5f9',
          bodyColor: '#94a3b8',
          borderColor: 'rgba(255,255,255,0.1)',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${formatPrice(ctx.raw)}`,
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: { unit: 'quarter', displayFormats: { quarter: 'MMM yy' } },
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#64748b', font: { size: 10 } },
          stacked: true,
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: {
            color: '#64748b',
            font: { size: 10 },
            callback: (v) => formatPriceShort(v),
          },
          stacked: true,
        },
      },
    },
  });
}

// ── AI Executive Summary ─────────────────────────────────────────
function renderAIInsight() {
  const panel = document.getElementById('ai-insight-text');
  if (!panel) return;
  const insight = DATA.aiInsight || 'AI Insight tidak tersedia. Silakan konfigurasi Azure OpenAI API Key.';
  
  // Convert newlines to HTML paragraphs for rich display
  const paragraphs = insight.split('\n\n').filter(p => p.trim());
  const htmlContent = paragraphs.map(p => `<p style="margin-bottom: 12px">${p}</p>`).join('');
  
  // Fade-in reveal effect
  panel.style.opacity = '0';
  panel.innerHTML = htmlContent;
  
  setTimeout(() => {
    panel.style.transition = 'opacity 0.8s ease';
    panel.style.opacity = '1';
  }, 300);
}

// ── Navigation between tab sections ──────────────────────────────
function switchSection(sectionId) {
  document.querySelectorAll('.nav-section-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.section === sectionId);
  });
  // Smooth scroll to section
  const target = document.getElementById(sectionId);
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// ── Init on DOM Load ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', initApp);
