import { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import SearchBar from '../../components/SearchBar/SearchBar';
import AnalysisResult from '../../components/AnalysisResult/AnalysisResult';
import { analyzeStock, getStockReport } from '../../services/api';
import './Dashboard.css';

export default function Dashboard() {
    const [loading, setLoading] = useState(false);
    const [analysisData, setAnalysisData] = useState(null);
    const [reportData, setReportData] = useState(null);
    const [error, setError] = useState(null);
    const [searchedSymbol, setSearchedSymbol] = useState('');

    const handleSearch = async (symbol, period) => {
        setLoading(true);
        setError(null);
        setReportData(null);
        setSearchedSymbol(symbol);

        try {
            // Fetch analysis and report in parallel
            const [analysis, report] = await Promise.allSettled([
                analyzeStock(symbol, period),
                getStockReport(symbol, period),
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

    return (
        <div className="dashboard">
            <div className="dashboard-container">
                <SearchBar onSearch={handleSearch} loading={loading} />

                {/* Loading State */}
                {loading && (
                    <div className="loading-state animate-fade-in">
                        <div className="loading-card">
                            <div className="loading-dots">
                                <div className="loading-dot" />
                                <div className="loading-dot" />
                                <div className="loading-dot" />
                            </div>
                            <p className="loading-text">
                                Analyzing <strong>{searchedSymbol}</strong>...
                            </p>
                            <p className="loading-subtext">
                                Fetching data, computing indicators, and generating recommendations
                            </p>
                        </div>
                    </div>
                )}

                {/* Error State */}
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

                {/* Results */}
                {analysisData && !loading && (
                    <AnalysisResult data={analysisData} report={reportData} />
                )}

                {/* Empty State */}
                {!analysisData && !loading && !error && (
                    <div className="empty-state animate-fade-in">
                        <div className="empty-illustration">
                            <div className="empty-circle" />
                            <div className="empty-line" />
                            <div className="empty-line short" />
                        </div>
                        <p className="empty-text">
                            Search for a stock ticker to get started
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
