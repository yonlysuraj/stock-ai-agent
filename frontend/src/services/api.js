const API_BASE = 'http://localhost:8000';

async function handleResponse(response) {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed with status ${response.status}`);
  }
  return response.json();
}

export async function analyzeStock(symbol, period = '1y') {
  const response = await fetch(`${API_BASE}/api/stocks/analyze/${encodeURIComponent(symbol)}?period=${period}`);
  return handleResponse(response);
}

export async function getStockReport(symbol, period = '1y') {
  const response = await fetch(`${API_BASE}/api/stocks/report/${encodeURIComponent(symbol)}?period=${period}`);
  return handleResponse(response);
}

export async function analyzeSentiment(texts) {
  const response = await fetch(`${API_BASE}/api/stocks/sentiment/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texts }),
  });
  return handleResponse(response);
}

export async function getStockNews(symbol, limit = 10) {
  const response = await fetch(`${API_BASE}/api/stocks/news/${encodeURIComponent(symbol)}?limit=${limit}`);
  return handleResponse(response);
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`);
  return handleResponse(response);
}
