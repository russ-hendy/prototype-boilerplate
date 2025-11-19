import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

export function useAuth() {
  const auth = useAuthStore();

  const user = computed(() => auth.user);
  const authEnabled = computed(() => auth.authEnabled);
  const isAuthenticated = computed(() => auth.isAuthenticated);

  // Example helper: get Firebase ID token (returns null if unavailable)
  async function getToken() {
    if (!authEnabled.value || !auth.user) return null;
    try {
      return await auth.user.getIdToken(); 
    } catch (e) {
      console.error("Error getting token:", e);
      return null;
    }
  }

  // Optional structured login/logout helpers
  function login(user) {
    auth.setUser(user);
  }

  function logout() {
    auth.clearUser();
  }

  return {
    user,
    authEnabled,
    isAuthenticated,
    login,
    logout,
    getToken
  };
}
