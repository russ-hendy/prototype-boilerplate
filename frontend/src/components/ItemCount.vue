<script setup>
import { ref, onMounted } from 'vue';

// Define a reactive variable to hold the item count
const itemCount = ref(0);
const isLoading = ref(true);
const error = ref(null);

// Define the API URL using the right ENV 
const API_URL = import.meta.env.VITE_API_URL + '/items';

const fetchItemCount = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    // 1. Fetch the data from the FastAPI endpoint
    const response = await fetch(API_URL);
    
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