import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
// initialise auth. Depends on VITE_AUTH_ENABLED in the relevant frontend .env file
useAuthStore().initAuth()
app.mount('#app')
