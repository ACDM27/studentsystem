<template>
  <div class="home-container">
    <div class="content-box">
      <div class="platform-title">
        <div class="icon-box">
          <n-icon size="32" class="title-icon">
            <IconSchool :size="32" />
          </n-icon>
        </div>
        <h1>学生综合信息服务平台</h1>
      </div>
      <p class="platform-desc">为学生提供一站式综合服务，助力学业发展与成长</p>
      
      <div class="platform-content">
        <div class="avatar-container">
          <n-avatar size="large" round>
            <n-icon size="30">
              <IconUser :size="30" />
            </n-icon>
          </n-avatar>
        </div>
        
        <div class="feature-icons">
          <div class="feature-item">
            <n-icon size="32" class="feature-icon">
              <IconBook :size="32" />
            </n-icon>
            <span>学习管理</span>
          </div>
          <div class="feature-item">
            <n-icon size="32" class="feature-icon">
              <IconBell :size="32" />
            </n-icon>
            <span>课程提示</span>
          </div>
          <div class="feature-item">
            <n-icon size="32" class="feature-icon">
              <IconMessageCircle :size="32" />
            </n-icon>
            <span>交流咨询</span>
          </div>
          <div class="feature-item">
            <n-icon size="32" class="feature-icon">
              <IconTrendingUp :size="32" />
            </n-icon>
            <span>就业动向</span>
          </div>
        </div>
        
        <div class="action-buttons">
          <!-- 学生端登录 -->
          <n-button 
            type="primary" 
            size="large" 
            class="login-btn student-btn" 
            @click="goToStudentLogin"
          >
            <template #icon>
              <n-icon><IconUser /></n-icon>
            </template>
            学生登录
          </n-button>
          
          <!-- 管理端登录 -->
          <n-button 
            size="large" 
            class="login-btn admin-btn" 
            @click="goToAdminLogin"
            color="#1e2730"
          >
            <template #icon>
              <n-icon><IconShield /></n-icon>
            </template>
            管理端登录
          </n-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import {
  IconUser,
  IconBook,
  IconBell,
  IconMessageCircle,
  IconTrendingUp,
  IconSchool,
  IconShield
} from '@tabler/icons-vue'

const router = useRouter()

// 跳转到学生端登录
const goToStudentLogin = () => {
  router.push('/student/login')
}

// 跳转到管理端登录
const goToAdminLogin = () => {
  router.push('/admin/login')
}
</script>

<style scoped>
/* 🔑 优化：确保页面滚动条完全隐藏 */
.home-container {
  min-height: 100vh;
  height: 100vh; /* 固定高度，防止出现滚动条 */
  width: 100%;
  background: linear-gradient(135deg, #e6f7ff 0%, #d0e8ff 50%, #c2e0ff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  overflow: hidden; /* 隐藏溢出内容 */
  box-sizing: border-box; /* 确保 padding 不会导致溢出 */
}

.content-box {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  padding: 40px 30px;
  text-align: center;
}

.platform-title {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.icon-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  background-color: #1890ff;
  border-radius: 4px;
  margin-right: 12px;
}

.title-icon {
  color: white;
}

.platform-title h1 {
  font-size: 28px;
  font-weight: bold;
  color: #1e293b;
  margin: 0;
}

.platform-desc {
  color: #64748b;
  font-size: 16px;
  margin-bottom: 30px;
}

.avatar-container {
  margin-bottom: 20px;
}

.service-title {
  font-size: 20px;
  font-weight: bold;
  color: #1e293b;
  margin-bottom: 8px;
}

.service-desc {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 30px;
}

.feature-icons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 25%;
}

.feature-icon {
  color: #1890ff;
  margin-bottom: 8px;
}

.feature-item span {
  font-size: 14px;
  color: #64748b;
  margin-top: 5px;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.login-btn {
  flex: 1;
  transition: all 0.3s ease;
}

.student-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.admin-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(30, 39, 48, 0.3);
}
</style>