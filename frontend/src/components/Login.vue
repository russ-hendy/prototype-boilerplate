<script setup>
import { ref, onMounted } from 'vue';
import { useAuth } from '@/composables/useAuth';

import { 
    signInWithEmailAndPassword, 
    signOut,
    GoogleAuthProvider,
    signInWithPopup,
} from 'firebase/auth';
import { authInstance } from '../firebase'; 

// Reactive state variables
const email = ref('');
const password = ref('');
const loginError = ref(null);
const isLoading = ref(false);
const { authEnabled, user, login, logout } = useAuth();


onMounted(() => {
    if (authInstance) {
        // Simple listener to track user state changes
        authInstance.onAuthStateChanged((firebaseUser) => {
            if (firebaseUser) {
                login(firebaseUser);
            } else {
                logout();
            }
        });
    }
});

const handleLogin = async () => {
    if (!authInstance || !email.value || !password.value) return;
    
    isLoading.value = true;
    loginError.value = null;
    
    try {
        const userCredential = await signInWithEmailAndPassword(
            authInstance, 
            email.value, 
            password.value
        );
        login(userCredential.user);
        console.log("Logged in successfully:", user.value?.uid);
    } catch (error) {
        console.error("Login failed:", error.code);
        loginError.value = error.message;
    } finally {
        isLoading.value = false;
    }
};

const handleLogout = async () => {
    if (!authInstance) return;
    try {
        await signOut(authInstance);
        logout();
        console.log("Logged out.");
    } catch (error) {
        console.error("Logout failed:", error);
    }
};

const googleProvider = new GoogleAuthProvider();

const handleGoogleLogin = async () => {
    if (!authInstance) return;

    isLoading.value = true;
    loginError.value = null;

    try {
        // 1. Open the Google sign-in pop-up
        const userCredential = await signInWithPopup(authInstance, googleProvider);
        
        login(userCredential.user);
        console.log("Logged in successfully via Google:", user.value.uid);
    } catch (error) {
        console.error("Google login failed:", error.code);
        // Handle common errors like pop-up closed or account exists
        loginError.value = error.message; 
    } finally {
        isLoading.value = false;
    }
};

</script>

<template>
    <div class="auth-panel">
        <h3>🔐 Firebase Authentication</h3>
        
        <div v-if="!authEnabled" class="warning">
            Authentication is disabled (AUTH_ENABLED=false).
        </div>

        <div v-else-if="user" class="logged-in-state">
            <p>Welcome, {{ user.email }}</p>
            <p>UID: {{ user.uid }}</p>
            
            <button @click="handleLogout" class="logout-btn">
                Sign Out
            </button>
        </div>

        <form v-else @submit.prevent="handleLogin" class="login-form">
            <input type="email" v-model="email" placeholder="Email" required>
            <input type="password" v-model="password" placeholder="Password" required>
            
            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Logging In...' : 'Login' }}
            </button>
            
            <p>— OR —</p>
            
            <button 
                type="button" 
                @click="handleGoogleLogin" 
                :disabled="isLoading" 
                class="google-btn"
            >
                Sign in with Google 
            </button>
            
            <p v-if="loginError" class="error">{{ loginError }}</p>
        </form>
    </div>
</template>

<style scoped>
/* Basic styling for clarity */
.auth-panel { 
    margin: 20px auto; 
    padding: 20px; 
    border: 1px solid #ddd; 
    max-width: 400px; 
    text-align: center; 
}
.login-form input { margin-bottom: 10px; padding: 8px; width: 80%; display: block; margin-left: auto; margin-right: auto;}
.warning { color: orange; }
.error { color: red; }
/* Add a style for the Google button for visual distinction */
.google-btn {
    background-color: #4285F4;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    margin-top: 10px;
    width: 80%;
    margin-left: auto; 
    margin-right: auto;
}
.logout-btn {
    background-color: #dc3545; /* Bootstrap Red */
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    margin-top: 10px;
}
</style>