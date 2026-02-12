import {
    TrendingUp,
    TrendingDown,
    Minus,
    ArrowUpRight,
    ArrowDownRight,
    BarChart3,
    Activity,
    Target,
    Shield,
    Zap,
    Newspaper,
} from 'lucide-react';
import './AnalysisResult.css';

function getActionColor(action) {
    switch (action?.toUpperCase()) {
        case 'BUY': return 'success';
        case 'SELL': return 'danger';
        default: return 'warning';
    }
}

function getActionIcon(action) {
    switch (action?.toUpperCase()) {
        case 'BUY': return TrendingUp;
        case 'SELL': return TrendingDown;
        default: return Minus;
    }
}

function getRSIStatus(rsi) {
    if (rsi < 30) return { label: 'Oversold', color: 'success' };
    if (rsi > 70) return { label: 'Overbought', color: 'danger' };
    return { label: 'Neutral', color: 'warning' };
}

function getSentimentColor(sentiment) {
    switch (sentiment?.toUpperCase()) {
        case 'POSITIVE': return 'success';
        case 'NEGATIVE': return 'danger';
        default: return 'neutral';
    }
}

function ConfidenceBar({ confidence }) {
    const percent = Math.round(confidence * 100);
    return (
        <div className="confidence-bar-wrapper">
            <div className="confidence-bar-track">
                <div
                    className="confidence-bar-fill"
                    style={{ width: `${percent}%` }}
                />
            </div>
            <span className="confidence-percent">{percent}%</span>
        </div>
    );
}

function IndicatorCard({ icon: Icon, title, value, subtitle, status }) {
    return (
        <div className={`indicator-card ${status || ''}`}>
            <div className="indicator-header">
                <div className={`indicator-icon ${status || ''}`}>
                    <Icon size={16} />
                </div>
                <span className="indicator-title">{title}</span>
            </div>
            <div className="indicator-value">{value}</div>
            {subtitle && <div className="indicator-subtitle">{subtitle}</div>}
        </div>
    );
}

export default function AnalysisResult({ data, report }) {
    if (!data) return null;

    const { symbol, data: analysisData } = data;
    const { current_price, indicators, decision, price_history_length } = analysisData;
    const actionColor = getActionColor(decision.action);
    const ActionIcon = getActionIcon(decision.action);
    const rsiStatus = getRSIStatus(indicators.rsi);

    return (
        <div className="analysis-result animate-fade-in-up">
            {/* Header Card */}
            <div className="result-header-card">
                <div className="result-header-top">
                    <div className="result-symbol-group">
                        <h2 className="result-symbol">{symbol}</h2>
                        <span className={`action-badge ${actionColor}`}>
                            <ActionIcon size={14} />
                            {decision.action}
                        </span>
                    </div>
                    <div className="result-price-group">
                        <span className="result-price">${current_price?.toFixed(2)}</span>
                        <span className="result-meta">{price_history_length} data points</span>
                    </div>
                </div>

                <div className="decision-section">
                    <div className="decision-reason">{decision.reason}</div>
                    <div className="confidence-section">
                        <span className="confidence-label">Confidence</span>
                        <ConfidenceBar confidence={decision.confidence} />
                    </div>
                </div>
            </div>

            {/* Sentiment Section */}
            {analysisData.sentiment && (
                <div className="sentiment-section animate-fade-in-up delay-100">
                    <div className={`sentiment-card ${getSentimentColor(analysisData.sentiment.overall_sentiment)}`}>
                        <div className="sentiment-header">
                            <div className="sentiment-title-group">
                                <Newspaper size={20} />
                                <h3 className="sentiment-title">Market Sentiment</h3>
                            </div>
                            <span className={`sentiment-badge ${getSentimentColor(analysisData.sentiment.overall_sentiment)}`}>
                                {analysisData.sentiment.overall_sentiment} ({analysisData.sentiment.overall_score})
                            </span>
                        </div>
                        <p className="sentiment-summary">
                            {analysisData.sentiment.summary}
                        </p>
                    </div>
                </div>
            )}

            {/* Indicators Grid */}
            <div className="indicators-grid stagger-children">
                <IndicatorCard
                    icon={Activity}
                    title="RSI (14)"
                    value={indicators.rsi?.toFixed(2)}
                    subtitle={rsiStatus.label}
                    status={rsiStatus.color}
                />
                <IndicatorCard
                    icon={BarChart3}
                    title="MA 20"
                    value={`$${indicators.ma20?.toFixed(2)}`}
                    subtitle={
                        current_price > indicators.ma20
                            ? 'Price above MA20 — Uptrend'
                            : 'Price below MA20 — Downtrend'
                    }
                    status={current_price > indicators.ma20 ? 'success' : 'danger'}
                />
                <IndicatorCard
                    icon={Zap}
                    title="MACD"
                    value={indicators.macd != null ? indicators.macd.toFixed(4) : 'N/A'}
                    subtitle={
                        indicators.macd == null
                            ? 'Needs 26+ data points'
                            : indicators.macd > 0
                                ? 'Bullish momentum'
                                : 'Bearish momentum'
                    }
                    status={
                        indicators.macd == null
                            ? 'warning'
                            : indicators.macd > 0
                                ? 'success'
                                : 'danger'
                    }
                />
            </div>

            {/* Report Section */}
            {report && (
                <div className="report-section animate-fade-in-up">
                    <h3 className="report-section-title">
                        <Shield size={18} />
                        Detailed Report
                    </h3>

                    {report.summary && (
                        <div className="report-card">
                            <h4 className="report-card-title">Summary</h4>
                            <p className="report-card-text">{report.summary}</p>
                        </div>
                    )}

                    {report.indicators && (
                        <div className="report-card">
                            <h4 className="report-card-title">Technical Analysis</h4>
                            <div className="report-indicators-list">
                                {report.indicators.map((ind, i) => (
                                    <div key={i} className="report-indicator-row">
                                        <span className="report-ind-name">{ind.name}</span>
                                        <span className="report-ind-value">{ind.value}</span>
                                        <span className="report-ind-interpretation">{ind.interpretation}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {report.risk_assessment && (
                        <div className="report-card">
                            <h4 className="report-card-title">Risk Assessment</h4>
                            <p className="report-card-text">{report.risk_assessment}</p>
                        </div>
                    )}

                    {report.recommendation && (
                        <div className="report-card">
                            <h4 className="report-card-title">Recommendation</h4>
                            <p className="report-card-text">{report.recommendation}</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
