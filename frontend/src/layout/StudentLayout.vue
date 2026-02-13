<template>
  <div class="layout-container">
    <student-sidebar class="sidebar" />
    <div class="content">
      <router-view />
    </div>
    <!-- 全局悬浮AI助手 -->
    <FloatingAiAssistant />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import StudentSidebar from './student-sidebar.vue'
import FloatingAiAssistant from '@/components/common/FloatingAiAssistant.vue'
</script>

<style scoped>
.layout-container {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  flex-shrink: 0;
}

.content {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
}
</style>