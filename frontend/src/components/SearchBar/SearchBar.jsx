import { useState, useEffect } from 'react';
import { Search, ArrowRight, Loader2 } from 'lucide-react';
import './SearchBar.css';

export default function SearchBar({ onSearch, loading, initialSymbol }) {
    const [symbol, setSymbol] = useState(initialSymbol || '');
    const [period, setPeriod] = useState('1y');

    // Sync internal state if initialSymbol changes externally (e.g. from URL or Trending click)
    // Sync internal state if initialSymbol changes externally (e.g. from URL or Trending click)
    useEffect(() => {
        if (initialSymbol) {
            setSymbol(initialSymbol);
        } else {
            setSymbol('');
        }
    }, [initialSymbol]);

    const periods = [
        { value: '1mo', label: '1M' },
        { value: '3mo', label: '3M' },
        { value: '6mo', label: '6M' },
        { value: '1y', label: '1Y' },
        { value: '2y', label: '2Y' },
        { value: '5y', label: '5Y' },
    ];

    const handleSubmit = (e) => {
        e.preventDefault();
        if (symbol.trim()) {
            onSearch(symbol.trim().toUpperCase(), period);
        }
    };

    const quickSymbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META'];

    return (
        <div className="search-section">
            <div className="search-header">
                <h1 className="search-title">Stock Analysis</h1>
                <p className="search-subtitle">
                    Enter a ticker symbol to get AI-powered technical analysis
                </p>
            </div>

            <form className="search-form" onSubmit={handleSubmit}>
                <div className="search-input-wrapper">
                    <Search className="search-icon" size={18} />
                    <input
                        id="stock-search-input"
                        type="text"
                        className="search-input"
                        placeholder="Enter ticker symbol (e.g. AAPL)"
                        value={symbol}
                        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                        maxLength={5}
                        autoComplete="off"
                        spellCheck={false}
                    />
                    <button
                        id="search-submit-btn"
                        type="submit"
                        className="search-btn"
                        disabled={!symbol.trim() || loading}
                    >
                        {loading ? (
                            <Loader2 size={18} className="spinning" />
                        ) : (
                            <ArrowRight size={18} />
                        )}
                    </button>
                </div>

                <div className="period-selector">
                    {periods.map((p) => (
                        <button
                            key={p.value}
                            type="button"
                            className={`period-chip ${period === p.value ? 'active' : ''}`}
                            onClick={() => setPeriod(p.value)}
                        >
                            {p.label}
                        </button>
                    ))}
                </div>
            </form>

            <div className="quick-symbols">
                <span className="quick-label">Quick:</span>
                {quickSymbols.map((s) => (
                    <button
                        key={s}
                        type="button"
                        className="quick-chip"
                        onClick={() => {
                            setSymbol(s);
                            onSearch(s, period);
                        }}
                    >
                        {s}
                    </button>
                ))}
            </div>
        </div>
    );
}
