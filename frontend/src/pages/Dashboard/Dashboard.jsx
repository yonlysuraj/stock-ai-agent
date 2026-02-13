
import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';
import SearchBar from '../../components/SearchBar/SearchBar';
import AnalysisResult from '../../components/AnalysisResult/AnalysisResult';
import MarketOverview from '../../components/MarketOverview/MarketOverview';
import TrendingStocks from '../../components/TrendingStocks/TrendingStocks';
import NewsList from '../../components/NewsList/NewsList';
import { analyzeStock, getStockReport, getStockNews } from '../../services/api';
import './Dashboard.css';

export default function Dashboard() {
    const [searchParams, setSearchParams] = useSearchParams();
    const ticker = searchParams.get('ticker');
    const period = searchParams.get('period') || '1y';

    const [loading, setLoading] = useState(false);
    const [analysisData, setAnalysisData] = useState(null);
    const [reportData, setReportData] = useState(null);
    const [error, setError] = useState(null);

    // Dashboard Home Data States
    const [marketOverview, setMarketOverview] = useState([]);
    const [marketNews, setMarketNews] = useState([]);
    const [dashboardLoading, setDashboardLoading] = useState(true);

    // Fetch initial dashboard home data (Indices & News)
    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const indices = ['SPY', 'QQQ', 'DIA', 'BTC-USD'];
                const indexPromises = indices.map(symbol => analyzeStock(symbol, '1mo').catch(e => null));
                const newsPromise = getStockNews('SPY', 6).catch(e => []);

                const [spyData, qqqData, diaData, btcData, newsData] = await Promise.all([
                    ...indexPromises,
                    newsPromise
                ]);

                // Process index data
                const processedIndices = [spyData, qqqData, diaData, btcData]
                    .filter(data => data && data.status === 'success')
                    .map(data => {
                        const current = data.data.current_price;
                        const history = data.data.price_history || [];
                        let change = 0;
                        let changePercent = 0;

                        if (history.length >= 2) {
                            const prevClose = history[history.length - 2].close;
                            change = current - prevClose;
                            changePercent = (change / prevClose) * 100;
                        }

                        return {
                            symbol: data.symbol,
                            price: current,
                            change,
                            changePercent
                        };
                    });

                setMarketOverview(processedIndices);

                if (newsData && newsData.articles) {
                    setMarketNews(newsData.articles);
                }
            } catch (err) {
                console.error("Failed to load dashboard data:", err);
            } finally {
                setDashboardLoading(false);
            }
        };

        // Only fetch dashboard data if we are on the home view (no ticker)
        // OR always fetch it so it's ready when user goes back? 
        // Let's fetch it once on mount.
        fetchDashboardData();
    }, []);

    // Effect: Handle Analysis when URL changes
    useEffect(() => {
        if (!ticker) {
            // Reset to Home View
            setAnalysisData(null);
            setReportData(null);
            setError(null);
            return;
        }

        const fetchAnalysis = async () => {
            setLoading(true);
            setError(null);
            // We can optionally keep showing old data while loading new, but clearing is safer for UI consistency
            setAnalysisData(null);
            setReportData(null);

            try {
                // Fetch analysis and report in parallel
                const [analysis, report] = await Promise.allSettled([
                    analyzeStock(ticker, period),
                    getStockReport(ticker, period),
                ]);

                if (analysis.status === 'fulfilled') {
                    setAnalysisData(analysis.value);
                } else {
                    throw new Error(analysis.reason?.message || 'Analysis failed');
                }

                if (report.status === 'fulfilled') {
                    setReportData(report.value);
                }
            } catch (err) {
                setError(err.message || 'Something went wrong');
                setAnalysisData(null);
            } finally {
                setLoading(false);
            }
        };

        fetchAnalysis();
    }, [ticker, period]);


    const handleSearch = (symbol, newPeriod) => {
        // Update URL to trigger the effect
        setSearchParams({ ticker: symbol, period: newPeriod || '1y' });
    };

    const handleTrendingSelect = (symbol) => {
        setSearchParams({ ticker: symbol, period: '1y' });
    };

    return (
        <div className="dashboard">
            <div className="dashboard-container">
                <SearchBar
                    onSearch={handleSearch}
                    loading={loading}
                    initialSymbol={ticker || ''}
                />

                {/* Loading State for Search */}
                {loading && (
                    <div className="loading-state animate-fade-in">
                        <div className="loading-card">
                            <div className="loading-dots">
                                <div className="loading-dot" />
                                <div className="loading-dot" />
                                <div className="loading-dot" />
                            </div>
                            <p className="loading-text">
                                Analyzing <strong>{ticker}</strong>...
                            </p>
                            <p className="loading-subtext">
                                Fetching data, computing indicators, and generating recommendations
                            </p>
                        </div>
                    </div>
                )}

                {/* Error State for Search */}
                {error && !loading && (
                    <div className="error-state animate-fade-in-up">
                        <div className="error-card">
                            <AlertCircle size={24} />
                            <div>
                                <p className="error-title">Analysis Failed</p>
                                <p className="error-message">{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Analysis Results (Only show if we have data) */}
                {analysisData && !loading && (
                    <AnalysisResult data={analysisData} report={reportData} />
                )}

                {/* Dashboard Home (Show when no ticker is selected in URL) */}
                {!ticker && !loading && (
                    <div className="dashboard-home animate-fade-in">
                        {dashboardLoading ? (
                            <div className="dashboard-skeleton">
                                <div className="skeleton-bar" />
                                <div className="skeleton-grid" />
                            </div>
                        ) : (
                            <>
                                <MarketOverview data={marketOverview} onSelect={handleTrendingSelect} />
                                <TrendingStocks onSelect={handleTrendingSelect} />
                                <NewsList news={marketNews} />
                            </>
                        )}

                        {/* Fallback empty state */}
                        {!dashboardLoading && marketOverview.length === 0 && marketNews.length === 0 && (
                            <div className="empty-state">
                                <div className="empty-illustration">
                                    <div className="empty-circle" />
                                    <div className="empty-line" />
                                    <div className="empty-line short" />
                                </div>
                                <p className="empty-text">
                                    Search for a stock ticker to see analysis
                                </p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
