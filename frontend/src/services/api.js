import { useAuth } from '@/composables/useAuth';

const API_URL_BASE = import.meta.env.VITE_API_URL;

export async function apiFetch(endpoint, options = {}) {
  const { authEnabled, getToken } = useAuth();

  const headers = {
    ...(options.headers || {}),
    'Content-Type': options?.skipJson ? undefined : 'application/json'
  };

  // Auto-inject token if enabled
  if (authEnabled.value) {
    const token = await getToken();
    if (!token) {
      throw new Error("No token available: user must be logged in.");
    }
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(API_URL_BASE + endpoint, {
    ...options,
    headers
  });

  // Throw readable error for HTTP non-2xx
  if (!response.ok) {
    const text = await response.text().catch(() => 'Unknown error');
    throw new Error(`HTTP ${response.status}: ${text}`);
  }

  // ❗Important: return raw Response – caller decides how to read it
  return response;
}
