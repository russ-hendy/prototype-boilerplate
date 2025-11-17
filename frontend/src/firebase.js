import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth'; 

// 1. Read the auth enabled flag from the environment
export const AUTH_ENABLED = import.meta.env.VITE_AUTH_ENABLED === 'true';

// 2. Initialize Firebase (only if auth is enabled)
let app = null;
if (AUTH_ENABLED) {
  const firebaseConfig = {
    apiKey: import.meta.env.VITE_API_KEY,
    authDomain: import.meta.env.VITE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_APP_ID,
  };

  app = initializeApp(firebaseConfig);
  console.log('✅ Firebase initialized.');

} else {
  console.log('⚠️ Firebase AUTH is disabled via VITE_AUTH_ENABLED=false.');
}

let authInstance = null;
if (AUTH_ENABLED && app) {
    authInstance = getAuth(app);
    console.log('✅ Firebase Auth service ready.');
}

// Export the initialized app (or null)
export { app, authInstance };
// You would also export 'getAuth(app)' and 'signInWithEmailAndPassword', etc., here.