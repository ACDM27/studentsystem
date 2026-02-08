<template>
  <div class="admin-login-container">
    <!-- 左侧装饰区域 -->
    <div class="left-decoration">
      <div class="decoration-content">
        <div class="isometric-illustration">
          <!-- 3D建筑物1 -->
          <div class="building building-1">
            <div class="building-top"></div>
            <div class="building-side"></div>
            <div class="building-front"></div>
          </div>
          
          <!-- 3D建筑物2 -->
          <div class="building building-2">
            <div class="building-layers">
              <div class="layer"></div>
              <div class="layer"></div>
              <div class="layer"></div>
              <div class="layer"></div>
            </div>
          </div>
          
          <!-- 3D建筑物3 -->
          <div class="building building-3">
            <div class="building-top"></div>
            <div class="building-side"></div>
            <div class="building-front"></div>
          </div>
          
          <!-- 中心平台 -->
          <div class="center-platform">
            <div class="platform-ring"></div>
            <div class="platform-core"></div>
          </div>
          
          <!-- 连接线 -->
          <div class="connection-lines">
            <div class="line line-1"></div>
            <div class="line line-2"></div>
            <div class="line line-3"></div>
          </div>
        </div>
        
        <div class="welcome-text">
          <h1>学生综合信息服务平台</h1>
          <p>智能化管理 · 数据驱动决策</p>
        </div>
      </div>
    </div>

    <!-- 右侧登录表单区域 -->
    <div class="right-form">
      <div class="form-container">
        <div class="form-header">
          <h2>您好！</h2>
          <p class="form-subtitle">欢迎来到后台管理平台</p>
        </div>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入账号"
              prefix-icon="User"
              size="large"
              clearable
              class="form-input"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              size="large"
              show-password
              clearable
              class="form-input"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="warning"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
            >
              登 录
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <el-link type="info" @click="goToStudentLogin" class="switch-link">
            切换到学生端登录
          </el-link>
        </div>
      </div>
    </div>

    <!-- 底部版权信息 -->
    <div class="copyright">
      <p>© 2024 学生综合信息服务平台 | 版权所有</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { login } from '@/api'

const router = useRouter()

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在3-50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 128, message: '密码长度在6-128个字符', trigger: 'blur' }
  ]
}

// 表单引用
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

/**
 * 处理登录
 */
const handleLogin = async () => {
  if (!loginFormRef.value) return

  // 验证表单
  const valid = await loginFormRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    // 调用登录API
    const res = await login(loginForm)

    // 验证必须是管理员角色
    if (res.userInfo.role !== 'admin') {
      ElMessage.error('您不是管理员，无法访问管理端')
      return
    }

    // 存储Token和用户信息
    localStorage.setItem('token', res.access_token)
    localStorage.setItem('userInfo', JSON.stringify(res.userInfo))

    ElMessage.success('登录成功')

    // 跳转到管理端首页
    router.push('/admin/dashboard')
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.message || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

/**
 * 切换到学生端登录
 */
const goToStudentLogin = () => {
  router.push('/student/login')
}
</script>

<style scoped>
/* ==================== 主容器 ==================== */
.admin-login-container {
  position: relative;
  display: flex;
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #2196f3 100%);
  overflow: hidden;
}

/* 背景装饰元素 */
.admin-login-container::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 20s ease-in-out infinite;
}

.admin-login-container::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -5%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 15s ease-in-out infinite reverse;
}

/* ==================== 左侧装饰区域 ==================== */
.left-decoration {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  position: relative;
  z-index: 1;
}

.decoration-content {
  max-width: 600px;
}

/* 3D等距插图容器 */
.isometric-illustration {
  position: relative;
  width: 500px;
  height: 400px;
  margin: 0 auto 60px;
  transform: rotateX(60deg) rotateZ(-45deg);
  transform-style: preserve-3d;
}

/* 3D建筑物通用样式 */
.building {
  position: absolute;
  transform-style: preserve-3d;
  animation: buildingFloat 4s ease-in-out infinite;
}

.building-1 {
  left: 80px;
  top: 50px;
  animation-delay: 0s;
}

.building-2 {
  left: 200px;
  top: 80px;
  animation-delay: 0.3s;
}

.building-3 {
  left: 320px;
  top: 100px;
  animation-delay: 0.6s;
}

/* 建筑物1样式 */
.building-1 .building-top,
.building-1 .building-side,
.building-1 .building-front {
  position: absolute;
  background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%);
}

.building-1 .building-top {
  width: 80px;
  height: 80px;
  transform: translateZ(120px);
  background: linear-gradient(135deg, #90caf9 0%, #64b5f6 100%);
  box-shadow: 0 0 20px rgba(100, 181, 246, 0.5);
}

.building-1 .building-side {
  width: 80px;
  height: 120px;
  transform: rotateY(90deg) translateZ(0px);
  background: linear-gradient(135deg, #42a5f5 0%, #2196f3 100%);
}

.building-1 .building-front {
  width: 80px;
  height: 120px;
  transform: translateZ(0px);
  background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%);
}

/* 建筑物2 - 分层样式 */
.building-layers {
  position: relative;
  width: 100px;
}

.layer {
  width: 100px;
  height: 25px;
  margin-bottom: 5px;
  background: linear-gradient(135deg, #4fc3f7 0%, #29b6f6 100%);
  box-shadow: 0 2px 10px rgba(41, 182, 246, 0.3);
  position: relative;
}

.layer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
}

/* 建筑物3样式 */
.building-3 .building-top,
.building-3 .building-side,
.building-3 .building-front {
  position: absolute;
  background: linear-gradient(135deg, #4dd0e1 0%, #26c6da 100%);
}

.building-3 .building-top {
  width: 60px;
  height: 60px;
  transform: translateZ(90px);
  background: linear-gradient(135deg, #80deea 0%, #4dd0e1 100%);
  box-shadow: 0 0 15px rgba(77, 208, 225, 0.5);
}

.building-3 .building-side {
  width: 60px;
  height: 90px;
  transform: rotateY(90deg) translateZ(0px);
  background: linear-gradient(135deg, #26c6da 0%, #00bcd4 100%);
}

.building-3 .building-front {
  width: 60px;
  height: 90px;
  transform: translateZ(0px);
  background: linear-gradient(135deg, #4dd0e1 0%, #26c6da 100%);
}

/* 中心平台 */
.center-platform {
  position: absolute;
  left: 50%;
  top: 60%;
  transform: translate(-50%, -50%);
  width: 150px;
  height: 150px;
}

.platform-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid rgba(100, 181, 246, 0.5);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.platform-core {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: radial-gradient(circle, #64b5f6 0%, #2196f3 100%);
  border-radius: 50%;
  box-shadow: 0 0 30px rgba(33, 150, 243, 0.8);
  animation: coreGlow 3s ease-in-out infinite;
}

/* 连接线 */
.connection-lines {
  position: absolute;
  width: 100%;
  height: 100%;
}

.line {
  position: absolute;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(100, 181, 246, 0.6) 50%, transparent 100%);
  transform-origin: left center;
}

.line-1 {
  left: 120px;
  top: 110px;
  width: 100px;
  transform: rotate(45deg);
  animation: lineGlow 2s ease-in-out infinite;
}

.line-2 {
  left: 240px;
  top: 140px;
  width: 80px;
  transform: rotate(-30deg);
  animation: lineGlow 2s ease-in-out infinite 0.3s;
}

.line-3 {
  left: 360px;
  top: 160px;
  width: 70px;
  transform: rotate(60deg);
  animation: lineGlow 2s ease-in-out infinite 0.6s;
}

/* 欢迎文字 */
.welcome-text {
  text-align: center;
  color: white;
  margin-top: 40px;
}

.welcome-text h1 {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 16px 0;
  text-shadow: 0 4px 20px rgba(0,0,0,0.3);
  letter-spacing: 2px;
}

.welcome-text p {
  font-size: 18px;
  opacity: 0.9;
  margin: 0;
  font-weight: 300;
  letter-spacing: 1px;
}

/* ==================== 右侧表单区域 ==================== */
.right-form {
  width: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  box-shadow: -10px 0 40px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
}

.form-container {
  width: 100%;
  max-width: 360px;
  padding: 40px;
}

.form-header {
  margin-bottom: 40px;
}

.form-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #1e3a8a;
  margin: 0 0 8px 0;
}

.form-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

/* 表单样式 */
.login-form {
  margin-top: 32px;
}

.form-input {
  border-radius: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.2);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

/* 表单底部 */
.form-footer {
  text-align: center;
  margin-top: 24px;
}

.switch-link {
  font-size: 14px;
  color: #64748b;
  text-decoration: none;
  transition: color 0.3s ease;
}

.switch-link:hover {
  color: #2196f3;
}

/* ==================== 版权信息 ==================== */
.copyright {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  text-align: center;
}

.copyright p {
  margin: 0;
}

/* ==================== 动画效果 ==================== */
@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes buildingFloat {
  0%, 100% {
    transform: translateY(0) translateZ(0);
  }
  50% {
    transform: translateY(-10px) translateZ(10px);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

@keyframes coreGlow {
  0%, 100% {
    box-shadow: 0 0 30px rgba(33, 150, 243, 0.8);
  }
  50% {
    box-shadow: 0 0 50px rgba(33, 150, 243, 1);
  }
}

@keyframes lineGlow {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 1;
  }
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 1024px) {
  .left-decoration {
    display: none;
  }
  
  .right-form {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .right-form {
    background: rgba(255, 255, 255, 0.95);
  }
  
  .form-container {
    padding: 30px 20px;
  }
  
  .form-header h2 {
    font-size: 28px;
  }
}
</style>
