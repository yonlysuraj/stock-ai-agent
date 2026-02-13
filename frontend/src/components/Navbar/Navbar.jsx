import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BarChart3, TrendingUp, MessageSquareText, Activity, Menu, X } from 'lucide-react';
import './Navbar.css';

export default function Navbar() {
    const location = useLocation();
    const [isOpen, setIsOpen] = useState(false);

    const navLinks = [
        { to: '/', label: 'Dashboard', icon: BarChart3 },
        { to: '/watchlist', label: 'Watchlist', icon: TrendingUp },
        { to: '/sentiment', label: 'Sentiment', icon: MessageSquareText },
    ];

    const toggleMenu = () => setIsOpen(!isOpen);

    // Close menu when route changes
    useEffect(() => {
        setIsOpen(false);
    }, [location.pathname]);

    return (
        <nav className="navbar">
            <div className="navbar-inner">
                <Link to="/" className="navbar-brand">
                    <div className="navbar-logo">
                        <Activity size={20} strokeWidth={2.5} />
                    </div>
                    <span className="navbar-title">StockAI</span>
                </Link>

                {/* Mobile Menu Toggle */}
                <button className="navbar-toggle" onClick={toggleMenu} aria-label="Toggle menu">
                    {isOpen ? <X size={24} /> : <Menu size={24} />}
                </button>

                {/* Desktop & Mobile Links Container */}
                <div className={`navbar-content ${isOpen ? 'open' : ''}`}>
                    <div className="navbar-links">
                        {navLinks.map((link) => {
                            const Icon = link.icon;
                            const isActive = location.pathname === link.to;
                            return (
                                <Link
                                    key={link.to}
                                    to={link.to}
                                    className={`navbar-link ${isActive ? 'active' : ''}`}
                                >
                                    <Icon size={16} />
                                    <span>{link.label}</span>
                                </Link>
                            );
                        })}
                    </div>

                    <div className="navbar-status">
                        <div className="status-dot" />
                        <span className="status-text">Live</span>
                    </div>
                </div>
            </div>
        </nav>
    );
}
