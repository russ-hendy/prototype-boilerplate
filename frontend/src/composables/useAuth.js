import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth';

export function useAuth() {
  const auth = useAuthStore();
  const { user, authEnabled, isAuthenticated } = storeToRefs(auth);

  async function getToken() {
    return await auth.getFreshToken();
  }

  return {
    user,
    authEnabled,
    isAuthenticated,
    login: auth.setUser,
    logout: auth.clearUser,
    getToken,
  };
}
