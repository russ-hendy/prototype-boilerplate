import { useAuthStore } from '@/stores/auth';

const API_URL_BASE = import.meta.env.VITE_API_URL;

export async function apiFetch(endpoint, options = {}) {
  const auth = useAuthStore();

  const headers = {
    ...(options.headers || {})
  };

  if (!options.skipJson) {
    headers['Content-Type'] = 'application/json';
  }

  // Auto-inject token (if enabled)
  if (auth.authEnabled) {
    const token = await auth.getFreshToken();
    if (!token) {
      throw new Error("No token available: user must be logged in.");
    }
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(API_URL_BASE + endpoint, {
    ...options,
    headers
  });

  // Throw readable error for HTTP failures
  if (!response.ok) {
    const text = await response.text().catch(() => 'Unknown error');
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  return response; // caller decides how to read it
}
