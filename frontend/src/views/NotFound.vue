<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="not-found">
    <h1>404 - Page Not Found</h1>
    <p>Oops! We couldn't find that page.</p>
    
    <RouterLink to="/">Go back Home</RouterLink>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  padding: 50px;
}
</style>