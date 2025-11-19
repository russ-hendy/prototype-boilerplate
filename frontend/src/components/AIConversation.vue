<template>
  <div class="generator-container">
    <h2>AI Text Generator</h2>
    
    <div class="input-group">
      <textarea
        v-model="prompt"
        placeholder="Enter your prompt here..."
        rows="4"
        class="prompt-input"
      ></textarea>
      
      <div class="controls">
        <label class="checkbox-label">
          <input type="checkbox" v-model="streamResponse" />
          Stream response
        </label>
        
        <button 
          @click="sendPrompt" 
          :disabled="loading || !prompt.trim()"
          class="send-button"
        >
          {{ loading ? 'Generating...' : 'Send' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="result" class="result-container">
      <h3>Result:</h3>
      <p>{{ result }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { apiFetch } from '@/services/api';

// Define the API URL using the right ENV 
const API_URL_BASE = import.meta.env.VITE_API_URL;

const prompt = ref('');
const result = ref('');
const loading = ref(false);
const error = ref('');
const streamResponse = ref(false);

const sendPrompt = async () => {
  loading.value = true;
  error.value = '';
  result.value = '';

  try {
    if (streamResponse.value) {
      await sendStreamingRequest();
    } else {
      await sendRegularRequest();
    }
  } catch (err) {
    error.value = `Error: ${err.message}`;
    console.error('Error sending prompt:', err);
  } finally {
    loading.value = false;
  }
};

const sendRegularRequest = async () => {
  const response = await apiFetch('/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: prompt.value
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  result.value = data.result;
};

const sendStreamingRequest = async () => {
  const response = await apiFetch('/generate-stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: prompt.value
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    
    if (done) break;
    
    const chunk = decoder.decode(value, { stream: true });
    result.value += chunk;
  }
};
</script>

<style scoped>
.generator-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
  width: 18px;
  height: 18px;
}

.prompt-input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
}

.prompt-input:focus {
  outline: none;
  border-color: #4CAF50;
}

.send-button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover:not(:disabled) {
  background-color: #45a049;
}

.send-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
}

.result-container {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.result-container h3 {
  margin-top: 0;
  color: #333;
}

.result-container p {
  white-space: pre-wrap;
  line-height: 1.6;
}
</style>