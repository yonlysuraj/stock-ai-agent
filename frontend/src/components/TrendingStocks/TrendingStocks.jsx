import './TrendingStocks.css';
import { TrendingUp } from 'lucide-react';

const TRENDING_TICKERS = [
    { symbol: 'NVDA', name: 'NVIDIA' },
    { symbol: 'TSLA', name: 'Tesla' },
    { symbol: 'AAPL', name: 'Apple' },
    { symbol: 'MSFT', name: 'Microsoft' },
    { symbol: 'AMD', name: 'AMD' },
    { symbol: 'AMZN', name: 'Amazon' },
    { symbol: 'GOOGL', name: 'Google' },
    { symbol: 'COIN', name: 'Coinbase' }
];

export default function TrendingStocks({ onSelect }) {
    return (
        <div className="trending-stocks">
            <h3 className="section-title">
                <TrendingUp size={20} className="icon" />
                Trending Now
            </h3>
            <div className="trending-grid">
                {TRENDING_TICKERS.map((ticker) => (
                    <button
                        key={ticker.symbol}
                        className="trending-item"
                        onClick={() => onSelect(ticker.symbol)}
                    >
                        <span className="ticker-symbol">{ticker.symbol}</span>
                        <span className="ticker-name">{ticker.name}</span>
                    </button>
                ))}
            </div>
        </div>
    );
}
