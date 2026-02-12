import { useState, useEffect } from 'react';
import {
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
    Filter,
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
    const [loading, setLoading] = useState(true);
    const [articles, setArticles] = useState([]);
    const [filteredArticles, setFilteredArticles] = useState([]);
    const [error, setError] = useState(null);
    const [selectedArticle, setSelectedArticle] = useState(null);
    const [sentimentResult, setSentimentResult] = useState(null);
    const [analyzingArticle, setAnalyzingArticle] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCompany, setSelectedCompany] = useState('ALL');

    const popularTickers = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'GOOGL', 'META', 'NFLX'];

    // Fetch news from all popular tickers on mount
    useEffect(() => {
        fetchAllNews();
    }, []);

    // Filter articles based on search and company
    useEffect(() => {
        let filtered = articles;

        if (searchQuery.trim()) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(
                (article) =>
                    article.title.toLowerCase().includes(query) ||
                    article.description?.toLowerCase().includes(query) ||
                    article.source.toLowerCase().includes(query)
            );
        }

        if (selectedCompany !== 'ALL') {
            filtered = filtered.filter((article) => article.ticker === selectedCompany);
        }

        setFilteredArticles(filtered);
    }, [searchQuery, selectedCompany, articles]);

    const fetchAllNews = async () => {
        setLoading(true);
        setError(null);
        try {
            const allArticles = [];
            // Fetch news from multiple tickers in parallel
            const promises = popularTickers.map(async (ticker) => {
                try {
                    const res = await getStockNews(ticker, 5); // Get 5 articles per ticker
                    return (res.articles || []).map((article) => ({
                        ...article,
                        ticker, // Add ticker to each article
                    }));
                } catch (err) {
                    console.error(`Failed to fetch news for ${ticker}:`, err);
                    return [];
                }
            });

            const results = await Promise.all(promises);
            results.forEach((tickerArticles) => {
                allArticles.push(...tickerArticles);
            });

            // Shuffle for variety
            allArticles.sort(() => Math.random() - 0.5);
            setArticles(allArticles);
            setFilteredArticles(allArticles);
        } catch (err) {
            setError('Failed to load news');
        } finally {
            setLoading(false);
        }
    };

    const handleArticleClick = async (article) => {
        setSelectedArticle(article);
        setAnalyzingArticle(true);
        setSentimentResult(null);

        try {
            const text = article.title + (article.description ? '. ' + article.description : '');
            const res = await analyzeSentiment([text]);
            setSentimentResult(res.analysis);
        } catch (err) {
            console.error('Sentiment analysis failed:', err);
        } finally {
            setAnalyzingArticle(false);
        }
    };

    const closeModal = () => {
        setSelectedArticle(null);
        setSentimentResult(null);
    };

    const getSentimentIcon = (sentiment) => {
        switch (sentiment?.toUpperCase()) {
            case 'POSITIVE':
                return TrendingUp;
            case 'NEGATIVE':
                return TrendingDown;
            default:
                return Minus;
        }
    };

    const getSentimentColor = (sentiment) => {
        switch (sentiment?.toUpperCase()) {
            case 'POSITIVE':
                return 'success';
            case 'NEGATIVE':
                return 'danger';
            default:
                return 'warning';
        }
    };

    return (
        <div className="sentiment-page">
            <div className="sentiment-header">
                <h1 className="sentiment-title">
                    <Sparkles size={28} />
                    Market Sentiment
                </h1>
                <p className="sentiment-subtitle">
                    Explore financial news and discover AI-powered sentiment insights
                </p>
            </div>

            {/* Filters */}
            <div className="filters-section">
                <div className="search-bar">
                    <Search className="search-icon" size={16} />
                    <input
                        type="text"
                        placeholder="Search news..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />
                </div>

                <div className="company-filter">
                    <Filter size={14} />
                    <select
                        value={selectedCompany}
                        onChange={(e) => setSelectedCompany(e.target.value)}
                        className="company-select"
                    >
                        <option value="ALL">All Companies</option>
                        {popularTickers.map((ticker) => (
                            <option key={ticker} value={ticker}>
                                {ticker}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Loading State */}
            {loading && (
                <div className="loading-container">
                    <Loader2 size={32} className="spinning" />
                    <p>Loading news from all markets...</p>
                </div>
            )}

            {/* Error State */}
            {error && <div className="error-message">{error}</div>}

            {/* Pinterest Grid */}
            {!loading && !error && (
                <div className="masonry-grid">
                    {filteredArticles.map((article, index) => (
                        <div
                            key={`${article.ticker}-${article.id || index}`}
                            className="news-card"
                            onClick={() => handleArticleClick(article)}
                        >
                            {article.thumbnail && (
                                <div className="news-card-image">
                                    <img src={article.thumbnail} alt={article.title} loading="lazy" />
                                    <div className="news-card-ticker">{article.ticker}</div>
                                </div>
                            )}
                            <div className="news-card-content">
                                <h3 className="news-card-title">{article.title}</h3>
                                {article.description && (
                                    <p className="news-card-description">{article.description}</p>
                                )}
                                <div className="news-card-footer">
                                    <span className="news-card-source">{article.source}</span>
                                    <span className="news-card-date">
                                        <Clock size={12} />
                                        {timeAgo(article.date)}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* No Results */}
            {!loading && !error && filteredArticles.length === 0 && (
                <div className="no-results">
                    <Newspaper size={48} />
                    <p>No news articles found</p>
                </div>
            )}

            {/* Sentiment Modal */}
            {selectedArticle && (
                <div className="modal-overlay" onClick={closeModal}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <button className="modal-close" onClick={closeModal}>
                            <X size={20} />
                        </button>

                        <div className="modal-article">
                            {selectedArticle.thumbnail && (
                                <img
                                    src={selectedArticle.thumbnail}
                                    alt={selectedArticle.title}
                                    className="modal-image"
                                />
                            )}
                            <div className="modal-ticker-badge">{selectedArticle.ticker}</div>
                            <h2 className="modal-title">{selectedArticle.title}</h2>
                            {selectedArticle.description && (
                                <p className="modal-description">{selectedArticle.description}</p>
                            )}
                            <div className="modal-meta">
                                <span className="modal-source">{selectedArticle.source}</span>
                                <span className="modal-date">
                                    <Clock size={14} />
                                    {timeAgo(selectedArticle.date)}
                                </span>
                                {selectedArticle.url && (
                                    <a
                                        href={selectedArticle.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="modal-link"
                                    >
                                        <ExternalLink size={14} />
                                        Read Full Article
                                    </a>
                                )}
                            </div>
                        </div>

                        <div className="modal-divider" />

                        <div className="modal-sentiment">
                            {analyzingArticle ? (
                                <div className="sentiment-loading">
                                    <Loader2 size={32} className="spinning" />
                                    <p>Analyzing sentiment...</p>
                                </div>
                            ) : sentimentResult ? (
                                <>
                                    <h3 className="sentiment-section-title">
                                        <Sparkles size={18} />
                                        AI Sentiment Analysis
                                    </h3>
                                    <div
                                        className={`sentiment-badge ${getSentimentColor(
                                            sentimentResult.overall_sentiment
                                        )}`}
                                    >
                                        {(() => {
                                            const Icon = getSentimentIcon(sentimentResult.overall_sentiment);
                                            return <Icon size={24} />;
                                        })()}
                                        <span className="sentiment-label">
                                            {sentimentResult.overall_sentiment}
                                        </span>
                                    </div>

                                    <div className="sentiment-stats">
                                        <div className="sentiment-stat">
                                            <span className="stat-label">Score</span>
                                            <span className="stat-value">
                                                {sentimentResult.individual_scores?.[0]?.toFixed(2)}
                                            </span>
                                        </div>
                                        <div className="sentiment-stat">
                                            <span className="stat-label">Confidence</span>
                                            <span className="stat-value">
                                                {(sentimentResult.confidence * 100)?.toFixed(0)}%
                                            </span>
                                        </div>
                                    </div>

                                    {sentimentResult.interpretations?.[0] && (
                                        <div className="sentiment-interpretation">
                                            <p>{sentimentResult.interpretations[0]}</p>
                                        </div>
                                    )}
                                </>
                            ) : null}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
