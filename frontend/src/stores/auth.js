import { defineStore } from 'pinia';

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
    }
  }
});
