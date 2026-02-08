<template>
  <div class="admin-layout">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="admin-header">
        <div class="header-left">
          <h2 class="logo">学生综合信息服务平台 - 管理端</h2>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ adminName }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-container class="main-container">
        <!-- 侧边栏 -->
        <admin-sidebar class="admin-sidebar" />

        <!-- 主内容区 -->
        <el-main class="admin-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { User, ArrowDown } from '@element-plus/icons-vue'
import AdminSidebar from './AdminSidebar.vue'
import { getAdminInfo, adminLogout } from '@/utils/admin-auth'

// 获取管理员信息
const adminInfo = computed(() => getAdminInfo())
const adminName = computed(() => adminInfo.value?.name || '管理员')

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  if (command === 'logout') {
    adminLogout()
  }
}
</script>

<style scoped>
.admin-layout {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1e2730;
  color: #ffffff;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-container {
  height: calc(100vh - 60px);
  overflow: hidden;
}

.admin-sidebar {
  flex-shrink: 0;
}

.admin-main {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
