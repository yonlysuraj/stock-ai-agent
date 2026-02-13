
import { ExternalLink, Newspaper } from 'lucide-react';
import './NewsList.css';

export default function NewsList({ news }) {
    if (!news || news.length === 0) return null;

    return (
        <div className="news-list">
            <h3 className="section-title">
                <Newspaper size={20} className="icon" />
                Latest Market News
            </h3>
            <div className="news-grid">
                {news.map((item, index) => {
                    // Extract relevant fields, handling potential variations in API response
                    const title = item.title || "No Title";
                    const summary = item.summary || item.description || "";
                    const source = item.source || "Unknown Source";
                    const url = item.url || item.link || "#";
                    const time = item.time || item.published_at || "";

                    return (
                        <a
                            key={index}
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="news-item"
                        >
                            <div className="news-content">
                                <h4 className="news-title">{title}</h4>
                                <p className="news-summary">{summary.slice(0, 120)}...</p>
                                <div className="news-meta">
                                    <span className="news-source">{source}</span>
                                    {time && <span className="news-time">{new Date(time).toLocaleDateString()}</span>}
                                </div>
                            </div>
                            <ExternalLink size={16} className="external-icon" />
                        </a>
                    );
                })}
            </div>
        </div>
    );
}
