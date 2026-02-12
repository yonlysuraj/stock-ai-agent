import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Dashboard from './pages/Dashboard/Dashboard';
import SentimentPage from './pages/SentimentPage/SentimentPage';

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sentiment" element={<SentimentPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
