<!-- src/App.vue -->
<template>
  <n-config-provider>
    <n-dialog-provider>
      <n-message-provider>
        <router-view />
      </n-message-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { NMessageProvider, NDialogProvider, NConfigProvider } from 'naive-ui'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
}

body:has(.admin-login-container) {
  overflow: hidden !important;
  height: 100vh !important;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

* {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

#app {
  min-height: 100vh;
  width: 100%;
}
</style>
