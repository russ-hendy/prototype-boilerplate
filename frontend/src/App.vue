<script setup>
import { ref } from 'vue';
import ItemCount from './components/ItemCount.vue';
import AIConversation from './components/AIConversation.vue';
import Login from './components/Login.vue'; // <-- Import Login

// Ref for the Login component instance
const loginComponent = ref(null);
</script>

<template>
  <header>
    <h1>Vue & FastAPI Boilerplate</h1>
  </header>
  
  <main>
    <Login ref="loginComponent" />
    <ItemCount />
    <AIConversation />
  </main>
</template>

<style scoped></style>
