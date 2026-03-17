<template>
  <div class="layout-container">
    <student-sidebar class="sidebar" />
    <div class="content">
      <router-view />
    </div>
    <!-- 全局悬浮AI助手（进入AI对话页时隐藏） -->
    <FloatingAiAssistant v-if="showFloatingAi" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import StudentSidebar from './student-sidebar.vue'
import FloatingAiAssistant from '@/components/common/FloatingAiAssistant.vue'

const route = useRoute()

// 当处于 AI 对话助手页面时，隐藏全站悬浮助手以避免逻辑冲突
const showFloatingAi = computed(() => {
  return route.path !== '/student/portrait/ai-chat'
})
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