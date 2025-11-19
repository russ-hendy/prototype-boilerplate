<script setup>
import { RouterLink } from 'vue-router'
import Login from './Login.vue' 
</script>

<template>
  <nav style="border-bottom: 1px solid #ccc; padding-bottom: 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
    <div class="links">
      <RouterLink to="/" style="margin-right: 10px">Home</RouterLink>
      <RouterLink to="/page-2" style="margin-right: 10px">AI Chat</RouterLink>
      <RouterLink to="/page-3">Page 3</RouterLink>
    </div>
    
    <div class="user-actions">
      <Login /> 
    </div>
  </nav>
</template>