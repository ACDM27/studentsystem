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
/* 🔑 全局优化：确保展示页和登录页不显示滚动条 */
/* 为特定页面（首页、登录页）隐藏滚动条 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
}

/* 针对首页和登录页面隐藏滚动条 */
body:has(.home-container),
body:has(.login-page) {
  overflow: hidden !important;
  height: 100vh !important;
}

/* 隐藏滚动条但保持可滚动性（针对其他需要滚动的页面） */
/* Webkit 浏览器（Chrome, Safari, Edge） */
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

/* Firefox */
* {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

/* 确保 #app 占满整个视口 */
#app {
  min-height: 100vh;
  width: 100%;
}
</style>