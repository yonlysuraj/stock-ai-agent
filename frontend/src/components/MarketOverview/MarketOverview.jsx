import { ArrowUpRight, ArrowDownRight, TrendingUp, TrendingDown } from 'lucide-react';
import './MarketOverview.css';

export default function MarketOverview({ data, onSelect }) {
    if (!data || data.length === 0) return null;

    return (
        <div className="market-overview">
            <h2 className="section-title">Market Overview</h2>
            <div className="market-cards">
                {data.map((item, index) => {
                    const change = item.change || 0;
                    const changePercent = item.changePercent || 0;
                    const isPositive = change >= 0;

                    return (
                        <div
                            key={index}
                            className="market-card clickable"
                            onClick={() => onSelect && onSelect(item.symbol)}
                            role="button"
                            tabIndex={0}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' || e.key === ' ') {
                                    onSelect && onSelect(item.symbol);
                                }
                            }}
                        >
                            <div className="card-header">
                                <span className="symbol">{item.symbol}</span>
                                {isPositive ? (
                                    <TrendingUp size={16} className="trend-icon positive" />
                                ) : (
                                    <TrendingDown size={16} className="trend-icon negative" />
                                )}
                            </div>
                            <div className="card-body">
                                <span className="price">${item.price.toFixed(2)}</span>
                                <div className={`change ${isPositive ? 'positive' : 'negative'}`}>
                                    {isPositive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                                    <span>{Math.abs(change).toFixed(2)} ({Math.abs(changePercent).toFixed(2)}%)</span>
                                </div>
                            </div>
                            <span className="card-cta">View Analysis →</span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
