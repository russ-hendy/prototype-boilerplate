<script setup>
import { ref, onMounted, watch } from 'vue';

// --- Define props to receive the user object ---
const props = defineProps({
    user: Object, // The Firebase user object
    authEnabled: Boolean // The AUTH_ENABLED flag
});
// ----------------------------------------------------

// Define a reactive variable to hold the item count
const itemCount = ref(0);
const isLoading = ref(true);
const error = ref(null);

// Define the API URL using the right ENV 
const API_URL_BASE = import.meta.env.VITE_API_URL;


const fetchItemCount = async () => {
  isLoading.value = true;
  error.value = null;

  // 1. Determine the endpoint and check for token requirement
  let endpoint = '/items'; // Public endpoint
  let headers = { 'Content-Type': 'application/json' };
  
  if (props.authEnabled) {
      endpoint = '/secure-items'; // Protected endpoint

      // In development with auth disabled, user is null. We can skip token retrieval.
      if (props.user) {
          // 2. Get the ID Token from the Firebase user object
          const token = await props.user.getIdToken(); 
          // 3. Add the token to the Authorization header
          headers['Authorization'] = `Bearer ${token}`;
      } else if (!props.user) {
          // If auth is enabled but user is null, we can't fetch the secure endpoint
          isLoading.value = false;
          error.value = 'Login required to access /secure-items.';
          return;
      }
  }
  
  try {
    // 1. Fetch the data from the FastAPI endpoint
    const response = await fetch(API_URL_BASE + endpoint, {
        method: 'GET',
        headers: headers // <-- Use the prepared headers
    });
    
    // Check for HTTP errors (e.g., 404, 500)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    // 2. Parse the JSON response
    const data = await response.json();
    
    // 3. Update the reactive variable with the count
    itemCount.value = data.count;
    
  } catch (err) {
    console.error("Error fetching items count:", err);
    error.value = 'Failed to connect to API or retrieve data.';
    itemCount.value = 0; // Reset count on error
  } finally {
    isLoading.value = false;
  }
};

// Fetch data when the component is mounted to the DOM
onMounted(fetchItemCount);

// Watch the user object: refresh data whenever the user logs in/out
watch(() => props.user, () => {
    fetchItemCount();
});

</script>

<template>
  <div class="items-count-panel">
    <h3>📦 Items Collection Status</h3>
    
    <div v-if="isLoading" class="status-message loading">
      Loading count...
    </div>
    
    <div v-else-if="error" class="status-message error">
      {{ error }}
      <p>Please ensure the FastAPI container is running and accessible on <code>http://localhost:8000</code>.</p>
    </div>
    
    <div v-else class="status-message success">
      Current document count: <strong>{{ itemCount }}</strong>
    </div>

    <button @click="fetchItemCount" :disabled="isLoading">Refresh Count</button>
  </div>
</template>

<style scoped>
.items-count-panel {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-width: 400px;
  margin: 20px auto;
  text-align: center;
}
.status-message {
  margin: 15px 0;
  padding: 10px;
  border-radius: 4px;
}
.loading { background-color: #f0f8ff; }
.error { background-color: #fdd; color: #a00; }
.success { background-color: #dfd; }
</style>