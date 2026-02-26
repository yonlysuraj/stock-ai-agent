import './Footer.css';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="footer-content">
                <p className="footer-copyright">
                    © {currentYear} Suraj Mallick
                </p>

                <div className="footer-links">
                    <a
                        href="https://github.com/yonlysuraj/stock-ai-agent"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        GitHub
                    </a>
                    <a
                        href="https://github.com/yonlysuraj/stock-ai-agent/blob/main/LICENSE"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="footer-badge"
                    >
                        MIT License
                    </a>
                </div>
            </div>
        </footer>
    );
}
