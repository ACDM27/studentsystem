<template>
  <el-aside width="240px" class="sidebar-container">
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      router
      background-color="#2c3e50"
      text-color="#ffffff"
      active-text-color="#409eff"
    >
      <el-menu-item index="/admin/dashboard">
        <el-icon><DataLine /></el-icon>
        <span>数据概览</span>
      </el-menu-item>

      <el-menu-item index="/admin/achievements">
        <el-icon><List /></el-icon>
        <span>成果审核</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { DataLine, List } from '@element-plus/icons-vue'

const route = useRoute()

// 当前激活的菜单项
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar-container {
  background-color: #2c3e50;
  height: 100%;
  overflow-y: auto;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 240px;
}
</style>
