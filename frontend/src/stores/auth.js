import { defineStore } from 'pinia';
import { authInstance } from '@/firebase';
import { onIdTokenChanged } from 'firebase/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    authEnabled: false
  }),

  getters: {
    isAuthenticated: (state) => state.authEnabled && !!state.user
  },

  actions: {
    initAuth() {
      this.authEnabled = import.meta.env.VITE_AUTH_ENABLED === 'true';
    },

    setUser(user) {
      this.user = user;
    },

    clearUser() {
      this.user = null;
    },

    async getFreshToken() {
      if (!this.user) return null;
      try {
        return await this.user.getIdToken(); // returns refreshed token if needed
      } catch {
        return null;
      }
    },
  }
});

// Attach listener ONCE for handling of auth token refresh
onIdTokenChanged(authInstance, (firebaseUser) => {
  const auth = useAuthStore();
  if (firebaseUser) {
    auth.setUser(firebaseUser);
  } else {
    auth.clearUser();
  }
});
