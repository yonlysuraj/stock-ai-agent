const STORAGE_KEY = 'stockai_watchlist_v1';

function readStorage() {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeStorage(list) {
  if (typeof window === 'undefined') return;
  try {
    const unique = Array.from(new Set(list.map((s) => s.toUpperCase())));
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(unique));
  } catch {
    // Ignore storage errors
  }
}

export function getWatchlist() {
  return readStorage();
}

export function addToWatchlist(symbol) {
  if (!symbol) return getWatchlist();
  const current = readStorage();
  const next = Array.from(new Set([...current, symbol.toUpperCase()]));
  writeStorage(next);
  return next;
}

export function removeFromWatchlist(symbol) {
  if (!symbol) return getWatchlist();
  const current = readStorage();
  const next = current.filter((s) => s.toUpperCase() !== symbol.toUpperCase());
  writeStorage(next);
  return next;
}

export function clearWatchlist() {
  writeStorage([]);
  return [];
}

