import './PriceChart.css';

// history: [{ date, open, high, low, close, volume, adj_close }]
export default function PriceChart({ history = [] }) {
  if (!history || history.length === 0) return null;

  const closes = history
    .map((p) => (typeof p.close === 'number' ? p.close : Number(p.close)))
    .filter((v) => !Number.isNaN(v));

  if (closes.length === 0) return null;

  const min = Math.min(...closes);
  const max = Math.max(...closes);
  const range = max - min || 1;

  const width = 400;
  const height = 140;
  const padding = 8;

  const points = closes.map((price, idx) => {
    const x = (idx / Math.max(closes.length - 1, 1)) * (width - padding * 2) + padding;
    const y =
      height -
      padding -
      ((price - min) / range) * (height - padding * 2);
    return `${x},${y}`;
  });

  const path = points.join(' ');

  const latest = history[history.length - 1];

  return (
    <div className="price-chart-card">
      <div className="price-chart-header">
        <span className="price-chart-title">Price History</span>
        {latest?.close != null && (
          <span className="price-chart-latest">
            Last close: ${Number(latest.close).toFixed(2)}
          </span>
        )}
      </div>
      <div className="price-chart-wrapper">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          preserveAspectRatio="none"
          className="price-chart-svg"
        >
          {/* Background gradient */}
          <defs>
            <linearGradient id="priceChartFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
            </linearGradient>
          </defs>

          {/* Area under line */}
          <path
            d={`M ${points[0]} L ${path} L ${
              points[points.length - 1].split(',')[0]
            },${height - padding} L ${
              points[0].split(',')[0]
            },${height - padding} Z`}
            fill="url(#priceChartFill)"
            stroke="none"
          />

          {/* Line */}
          <polyline
            points={path}
            fill="none"
            stroke="#2563eb"
            strokeWidth="2"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
        </svg>
      </div>
      <div className="price-chart-footer">
        <span>
          Range: ${min.toFixed(2)} – ${max.toFixed(2)}
        </span>
        <span>{history.length} points</span>
      </div>
    </div>
  );
}

