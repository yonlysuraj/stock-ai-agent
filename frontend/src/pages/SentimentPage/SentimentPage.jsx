import { useState } from 'react';
import {
    MessageSquareText,
    Plus,
    X,
    Loader2,
    TrendingUp,
    TrendingDown,
    Minus,
    Sparkles,
    Newspaper,
    Search,
    ExternalLink,
    Clock,
    CheckCircle2,
    ArrowRight,
} from 'lucide-react';
import { analyzeSentiment, getStockNews } from '../../services/api';
import './SentimentPage.css';

function timeAgo(dateStr) {
    if (!dateStr) return '';
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
}

export default function SentimentPage() {
    const [texts, setTexts] = useState(['']);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    // News state
    const [newsSymbol, setNewsSymbol] = useState('');
    const [newsLoading, setNewsLoading] = useState(false);
    const [articles, setArticles] = useState([]);
    const [newsError, setNewsError] = useState(null);
    const [selectedArticles, setSelectedArticles] = useState(new Set());

    const addText = () => setTexts([...texts, '']);
    const removeText = (index) => setTexts(texts.filter((_, i) => i !== index));
    const updateText = (index, value) => {
        const newTexts = [...texts];
        newTexts[index] = value;
        setTexts(newTexts);
    };

    const handleAnalyze = async (textsToAnalyze) => {
        const validTexts = (textsToAnalyze || texts).filter((t) => t.trim());
        if (validTexts.length === 0) return;

        setLoading(true);
        setError(null);
        try {
            const res = await analyzeSentiment(validTexts);
            setResult({ ...res.analysis, analyzedTexts: validTexts });
        } catch (err) {
            setError(err.message || 'Sentiment analysis failed');
        } finally {
            setLoading(false);
        }
    };

    const handleFetchNews = async (e) => {
        e.preventDefault();
        if (!newsSymbol.trim()) return;

        setNewsLoading(true);
        setNewsError(null);
        setSelectedArticles(new Set());
        setResult(null);
        try {
            const res = await getStockNews(newsSymbol.trim().toUpperCase());
            setArticles(res.articles || []);
            if (res.articles?.length === 0) {
                setNewsError('No news found for this ticker.');
            }
        } catch (err) {
            setNewsError(err.message || 'Failed to fetch news');
            setArticles([]);
        } finally {
            setNewsLoading(false);
        }
    };

    const toggleArticle = (index) => {
        setSelectedArticles((prev) => {
            const next = new Set(prev);
            if (next.has(index)) next.delete(index);
            else next.add(index);
            return next;
        });
    };

    const selectAll = () => {
        if (selectedArticles.size === articles.length) {
            setSelectedArticles(new Set());
        } else {
            setSelectedArticles(new Set(articles.map((_, i) => i)));
        }
    };

    const analyzeSelected = () => {
        const selectedTexts = articles
            .filter((_, i) => selectedArticles.has(i))
            .map((a) => a.title + (a.description ? '. ' + a.description : ''));
        if (selectedTexts.length === 0) return;

        // Also set these in the manual texts for reference
        setTexts(selectedTexts);
        handleAnalyze(selectedTexts);
    };

    const getSentimentIcon = (sentiment) => {
        switch (sentiment?.toUpperCase()) {
            case 'POSITIVE': return TrendingUp;
            case 'NEGATIVE': return TrendingDown;
            default: return Minus;
        }
    };

    const getSentimentColor = (sentiment) => {
        switch (sentiment?.toUpperCase()) {
            case 'POSITIVE': return 'success';
            case 'NEGATIVE': return 'danger';
            default: return 'warning';
        }
    };

    const quickTickers = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'GOOGL'];

    return (
        <div className="sentiment-page">
            <div className="sentiment-header">
                <h1 className="sentiment-title">
                    <Sparkles size={28} />
                    Sentiment Analysis
                </h1>
                <p className="sentiment-subtitle">
                    Scrape financial news and analyze sentiment with AI
                </p>
            </div>

            <div className="sentiment-content">
                {/* ===== News Scraper Section ===== */}
                <div className="news-scraper-section">
                    <div className="section-label">
                        <Newspaper size={16} />
                        <span>Scrape News</span>
                    </div>

                    <form className="news-search-form" onSubmit={handleFetchNews}>
                        <div className="news-search-wrapper">
                            <Search className="news-search-icon" size={16} />
                            <input
                                id="news-ticker-input"
                                type="text"
                                className="news-search-input"
                                placeholder="Enter stock ticker (e.g. AAPL)"
                                value={newsSymbol}
                                onChange={(e) => setNewsSymbol(e.target.value.toUpperCase())}
                                maxLength={5}
                                autoComplete="off"
                                spellCheck={false}
                            />
                            <button
                                id="fetch-news-btn"
                                type="submit"
                                className="news-fetch-btn"
                                disabled={!newsSymbol.trim() || newsLoading}
                            >
                                {newsLoading ? (
                                    <Loader2 size={16} className="spinning" />
                                ) : (
                                    <>
                                        <Newspaper size={14} />
                                        Fetch News
                                    </>
                                )}
                            </button>
                        </div>
                    </form>

                    <div className="quick-tickers">
                        {quickTickers.map((t) => (
                            <button
                                key={t}
                                className="quick-ticker-chip"
                                onClick={() => {
                                    setNewsSymbol(t);
                                    setNewsLoading(true);
                                    setNewsError(null);
                                    setSelectedArticles(new Set());
                                    setResult(null);
                                    getStockNews(t).then((res) => {
                                        setArticles(res.articles || []);
                                        if (res.articles?.length === 0) setNewsError('No news found.');
                                    }).catch((err) => {
                                        setNewsError(err.message);
                                        setArticles([]);
                                    }).finally(() => setNewsLoading(false));
                                }}
                            >
                                {t}
                            </button>
                        ))}
                    </div>

                    {newsError && (
                        <div className="news-error animate-fade-in-up">{newsError}</div>
                    )}

                    {/* News Articles List */}
                    {articles.length > 0 && (
                        <div className="news-results animate-fade-in-up">
                            <div className="news-results-header">
                                <span className="news-count">{articles.length} articles found</span>
                                <div className="news-actions">
                                    <button className="select-all-btn" onClick={selectAll}>
                                        {selectedArticles.size === articles.length ? 'Deselect All' : 'Select All'}
                                    </button>
                                    <button
                                        id="analyze-selected-btn"
                                        className="analyze-selected-btn"
                                        onClick={analyzeSelected}
                                        disabled={selectedArticles.size === 0 || loading}
                                    >
                                        {loading ? (
                                            <Loader2 size={14} className="spinning" />
                                        ) : (
                                            <ArrowRight size={14} />
                                        )}
                                        Analyze {selectedArticles.size > 0 ? `(${selectedArticles.size})` : ''}
                                    </button>
                                </div>
                            </div>

                            <div className="articles-list stagger-children">
                                {articles.map((article, index) => (
                                    <div
                                        key={article.id || index}
                                        className={`article-card ${selectedArticles.has(index) ? 'selected' : ''}`}
                                        onClick={() => toggleArticle(index)}
                                    >
                                        <div className="article-checkbox">
                                            <div className={`checkbox ${selectedArticles.has(index) ? 'checked' : ''}`}>
                                                {selectedArticles.has(index) && <CheckCircle2 size={16} />}
                                            </div>
                                        </div>

                                        {article.thumbnail && (
                                            <div className="article-thumb">
                                                <img src={article.thumbnail} alt="" loading="lazy" />
                                            </div>
                                        )}

                                        <div className="article-content">
                                            <h4 className="article-title">{article.title}</h4>
                                            {article.description && (
                                                <p className="article-desc">{article.description}</p>
                                            )}
                                            <div className="article-meta">
                                                <span className="article-source">{article.source}</span>
                                                <span className="article-date">
                                                    <Clock size={11} />
                                                    {timeAgo(article.date)}
                                                </span>
                                                {article.url && (
                                                    <a
                                                        href={article.url}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="article-link"
                                                        onClick={(e) => e.stopPropagation()}
                                                    >
                                                        <ExternalLink size={11} />
                                                        Read
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* ===== Manual Input Section ===== */}
                <details className="manual-section">
                    <summary className="manual-summary">
                        <MessageSquareText size={16} />
                        Or type text manually
                    </summary>

                    <div className="manual-content">
                        <div className="texts-list">
                            {texts.map((text, index) => (
                                <div key={index} className="text-input-row animate-fade-in-up">
                                    <span className="text-index">{index + 1}</span>
                                    <textarea
                                        className="text-textarea"
                                        placeholder="Enter financial news headline or text..."
                                        value={text}
                                        onChange={(e) => updateText(index, e.target.value)}
                                        rows={2}
                                    />
                                    {texts.length > 1 && (
                                        <button className="remove-text-btn" onClick={() => removeText(index)}>
                                            <X size={14} />
                                        </button>
                                    )}
                                </div>
                            ))}
                        </div>

                        <div className="input-actions">
                            <button className="add-text-btn" onClick={addText}>
                                <Plus size={16} />
                                Add Text
                            </button>
                            <button
                                id="analyze-manual-btn"
                                className="analyze-btn"
                                onClick={() => handleAnalyze()}
                                disabled={loading || texts.every((t) => !t.trim())}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 size={16} className="spinning" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <MessageSquareText size={16} />
                                        Analyze
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </details>

                {/* ===== Error ===== */}
                {error && (
                    <div className="sentiment-error animate-fade-in-up">
                        <p>{error}</p>
                    </div>
                )}

                {/* ===== Results ===== */}
                {result && (
                    <div className="sentiment-results animate-fade-in-up">
                        <div className="overall-sentiment-card">
                            <div className="overall-header">
                                <h3>Overall Sentiment</h3>
                            </div>
                            <div className="overall-body">
                                <div className={`overall-badge ${getSentimentColor(result.overall_sentiment)}`}>
                                    {(() => { const Icon = getSentimentIcon(result.overall_sentiment); return <Icon size={20} />; })()}
                                    {result.overall_sentiment}
                                </div>
                                <div className="overall-stats">
                                    <div className="overall-stat">
                                        <span className="stat-label">Score</span>
                                        <span className="stat-value">{result.overall_score?.toFixed(2)}</span>
                                    </div>
                                    <div className="overall-stat">
                                        <span className="stat-label">Texts</span>
                                        <span className="stat-value">{result.texts_analyzed}</span>
                                    </div>
                                    <div className="overall-stat">
                                        <span className="stat-label">Confidence</span>
                                        <span className="stat-value">{(result.confidence * 100)?.toFixed(0)}%</span>
                                    </div>
                                </div>
                            </div>
                            {result.summary && (
                                <div className="overall-summary">
                                    <p>{result.summary}</p>
                                </div>
                            )}
                        </div>

                        {result.individual_scores && (
                            <div className="individual-results">
                                <h3 className="individual-title">Individual Analysis</h3>
                                <div className="individual-list stagger-children">
                                    {result.individual_scores.map((score, i) => (
                                        <div key={i} className="individual-card">
                                            <div className="individual-top">
                                                <span className={`score-badge ${score >= 0 ? 'success' : 'danger'}`}>
                                                    {score >= 0 ? '+' : ''}{score?.toFixed(2)}
                                                </span>
                                                <span className="individual-text">
                                                    {result.analyzedTexts?.[i] || `Text ${i + 1}`}
                                                </span>
                                            </div>
                                            {result.interpretations?.[i] && (
                                                <p className="individual-interpretation">
                                                    {result.interpretations[i]}
                                                </p>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
