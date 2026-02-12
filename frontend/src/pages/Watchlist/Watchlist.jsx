import { useEffect, useState } from 'react';
import { TrendingUp, TrendingDown, Minus, Trash2, PlusCircle } from 'lucide-react';
import { analyzeStock } from '../../services/api';
import { getWatchlist, addToWatchlist, removeFromWatchlist } from '../../services/watchlist';
import './Watchlist.css';

function getRSIStatus(rsi) {
  if (rsi < 30) return { label: 'Oversold', color: 'oversold' };
  if (rsi > 70) return { label: 'Overbought', color: 'overbought' };
  return { label: 'Neutral', color: 'neutral' };
}

function getActionMeta(action) {
  const upper = action?.toUpperCase();
  if (upper === 'BUY') return { label: 'Buy', color: 'buy', Icon: TrendingUp };
  if (upper === 'SELL') return { label: 'Sell', color: 'sell', Icon: TrendingDown };
  return { label: 'Hold', color: 'hold', Icon: Minus };
}

export default function WatchlistPage() {
  const [watchlist, setWatchlist] = useState([]);
  const [analyses, setAnalyses] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [newSymbol, setNewSymbol] = useState('');
  const [compareSelection, setCompareSelection] = useState([]);

  useEffect(() => {
    const stored = getWatchlist();
    setWatchlist(stored);
    if (stored.length) {
      fetchAnalyses(stored);
    }
  }, []);

  const fetchAnalyses = async (symbols) => {
    setLoading(true);
    setError(null);
    try {
      const results = await Promise.allSettled(
        symbols.map((symbol) => analyzeStock(symbol, '1y'))
      );

      const nextAnalyses = { ...analyses };
      results.forEach((res, idx) => {
        const symbol = symbols[idx];
        if (res.status === 'fulfilled') {
          nextAnalyses[symbol] = res.value;
        }
      });
      setAnalyses(nextAnalyses);
    } catch (err) {
      setError(err.message || 'Failed to load watchlist data');
    } finally {
      setLoading(false);
    }
  };

  const handleAddSymbol = async (e) => {
    e.preventDefault();
    const trimmed = newSymbol.trim().toUpperCase();
    if (!trimmed) return;

    const updated = addToWatchlist(trimmed);
    setWatchlist(updated);
    setNewSymbol('');

    // Fetch analysis for the newly added symbol
    try {
      const res = await analyzeStock(trimmed, '1y');
      setAnalyses((prev) => ({ ...prev, [trimmed]: res }));
    } catch {
      // Ignore per-symbol errors here; the dashboard can still be used
    }
  };

  const handleRemoveSymbol = (symbol) => {
    const updated = removeFromWatchlist(symbol);
    setWatchlist(updated);
    setAnalyses((prev) => {
      const next = { ...prev };
      delete next[symbol];
      return next;
    });
    setCompareSelection((prev) => prev.filter((s) => s !== symbol));
  };

  const toggleCompare = (symbol) => {
    setCompareSelection((prev) => {
      if (prev.includes(symbol)) {
        return prev.filter((s) => s !== symbol);
      }
      if (prev.length >= 3) {
        return prev;
      }
      return [...prev, symbol];
    });
  };

  const hasData = watchlist.length > 0;

  return (
    <div className="watchlist-page">
      <div className="watchlist-header">
        <h1 className="watchlist-title">Watchlist</h1>
        <p className="watchlist-subtitle">
          Track multiple tickers and quickly compare AI recommendations.
        </p>
      </div>

      <form className="watchlist-add-form" onSubmit={handleAddSymbol}>
        <div className="watchlist-input-wrapper">
          <input
            type="text"
            placeholder="Add ticker (e.g. AAPL)"
            value={newSymbol}
            maxLength={5}
            onChange={(e) => setNewSymbol(e.target.value.toUpperCase())}
          />
        </div>
        <button type="submit" className="watchlist-add-btn">
          <PlusCircle size={16} />
          Add
        </button>
      </form>

      {loading && (
        <div className="watchlist-loading">Loading watchlist data...</div>
      )}

      {error && <div className="watchlist-error">{error}</div>}

      {!hasData && !loading && (
        <div className="watchlist-empty">
          <p>Your watchlist is empty.</p>
          <p className="watchlist-empty-hint">
            Add tickers here or from the Dashboard using the &quot;Add to Watchlist&quot; button.
          </p>
        </div>
      )}

      {hasData && (
        <>
          <div className="watchlist-grid">
            {watchlist.map((symbol) => {
              const analysis = analyses[symbol];
              const inner = analysis?.data;
              const decision = inner?.decision;
              const indicators = inner?.indicators;
              const actionMeta = decision ? getActionMeta(decision.action) : null;
              const rsiStatus =
                indicators && typeof indicators.rsi === 'number'
                  ? getRSIStatus(indicators.rsi)
                  : null;

              return (
                <div key={symbol} className="watchlist-card">
                  <div className="watchlist-card-header">
                    <div className="watchlist-card-symbol">{symbol}</div>
                    <button
                      type="button"
                      className="watchlist-card-remove"
                      onClick={() => handleRemoveSymbol(symbol)}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                  {analysis ? (
                    <>
                      <div className="watchlist-card-main">
                        {inner?.current_price != null && (
                          <div className="watchlist-price">
                            ${inner.current_price.toFixed(2)}
                          </div>
                        )}
                        {actionMeta && (
                          <div className={`watchlist-action ${actionMeta.color}`}>
                            {(() => {
                              const Icon = actionMeta.Icon;
                              return <Icon size={14} />;
                            })()}
                            <span>{actionMeta.label}</span>
                          </div>
                        )}
                      </div>
                      <div className="watchlist-metrics">
                        {decision?.confidence != null && (
                          <div className="watchlist-metric">
                            <span className="metric-label">Confidence</span>
                            <span className="metric-value">
                              {(decision.confidence * 100).toFixed(0)}%
                            </span>
                          </div>
                        )}
                        {rsiStatus && (
                          <div className="watchlist-metric">
                            <span className="metric-label">RSI</span>
                            <span
                              className={`metric-rsi-bar ${rsiStatus.color}`}
                              title={rsiStatus.label}
                            />
                          </div>
                        )}
                      </div>
                    </>
                  ) : (
                    <div className="watchlist-card-placeholder">
                      No analysis loaded yet.
                    </div>
                  )}

                  <button
                    type="button"
                    className={`watchlist-compare-toggle ${
                      compareSelection.includes(symbol) ? 'active' : ''
                    }`}
                    onClick={() => toggleCompare(symbol)}
                  >
                    {compareSelection.includes(symbol)
                      ? 'Selected for compare'
                      : 'Select to compare'}
                  </button>
                </div>
              );
            })}
          </div>

          {compareSelection.length > 0 && (
            <div className="compare-strip">
              <div className="compare-strip-header">
                <h2>Quick Compare</h2>
                <p>Select up to 3 tickers to compare side by side.</p>
              </div>
              <div className="compare-strip-row">
                {compareSelection.map((symbol) => {
                  const analysis = analyses[symbol];
                  const inner = analysis?.data;
                  const decision = inner?.decision;
                  const indicators = inner?.indicators;
                  const actionMeta = decision ? getActionMeta(decision.action) : null;
                  const rsiStatus =
                    indicators && typeof indicators.rsi === 'number'
                      ? getRSIStatus(indicators.rsi)
                      : null;

                  return (
                    <div key={symbol} className="compare-chip">
                      <div className="compare-symbol">{symbol}</div>
                      {actionMeta && (
                        <div className={`compare-action ${actionMeta.color}`}>
                          {(() => {
                            const Icon = actionMeta.Icon;
                            return <Icon size={14} />;
                          })()}
                          <span>{actionMeta.label}</span>
                        </div>
                      )}
                      {decision?.confidence != null && (
                        <div className="compare-confidence">
                          {(decision.confidence * 100).toFixed(0)}%
                        </div>
                      )}
                      {rsiStatus && (
                        <div className={`compare-rsi ${rsiStatus.color}`}>
                          {rsiStatus.label}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

