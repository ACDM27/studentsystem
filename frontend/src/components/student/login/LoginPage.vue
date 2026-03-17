<template>
  <div class="login-page">
    <div class="back-home" @click="goToHome">
      <n-icon size="20" class="back-icon">
        <IconArrowLeft :size="20" />
      </n-icon>
      <span>返回首页</span>
    </div>

    <div class="login-container">
      <div class="platform-header">
        <div class="icon-box">
          <n-icon size="32" class="platform-icon">
            <IconSchool :size="32" />
          </n-icon>
        </div>
        <h1>学生综合信息服务平台</h1>
      </div>

      <div class="login-box">
        <div class="avatar-container">
          <n-avatar size="large" round>
            <n-icon size="30">
              <IconUser :size="30" />
            </n-icon>
          </n-avatar>
        </div>

        <h2>学生登录</h2>

        <n-form class="login-form" :model="form" :rules="rules" ref="formRef">
          <n-form-item label="账号" path="student_number">
            <n-input v-model:value="form.student_number" placeholder="请输入账号" clearable>
              <template #prefix>
                <n-icon class="input-icon"><IconIdBadge2 :size="24" /></n-icon>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item label="密码" path="password">
            <n-input
              v-model:value="form.password"
              type="password"
              placeholder="请输入密码"
              clearable
              show-password-on="click"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <n-icon class="input-icon"><IconLock :size="24" /></n-icon>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item>
            <div class="remember-password">
              <n-checkbox v-model:checked="rememberPassword">记住密码</n-checkbox>
            </div>
          </n-form-item>
          <n-form-item>
            <n-button type="primary" block @click="handleLogin" color="#000000" :loading="loading">
              登录
            </n-button>
          </n-form-item>
        </n-form>

      </div>
    </div>

    <!-- 首次登录修改密码弹窗 -->
    <n-modal v-model:show="showChangePwdModal" :mask-closable="false" :close-on-esc="false">
      <n-card
        style="width: 420px; border-radius: 12px;"
        :bordered="false"
      >
        <div class="modal-header">
          <n-tag type="warning" size="small">首次登录</n-tag>
          <span class="modal-hint">检测到您使用初始密码登录，为保障账号安全请立即修改密码</span>
        </div>

        <h3 class="modal-title">修改登录密码</h3>

        <n-form :model="pwdForm" :rules="pwdRules" ref="pwdFormRef" class="pwd-form">
          <n-form-item label="新密码" path="new_password">
            <n-input
              v-model:value="pwdForm.new_password"
              type="password"
              placeholder="请设置新密码（至少6位）"
              show-password-on="click"
              clearable
            >
              <template #prefix><n-icon><IconLock :size="20" /></n-icon></template>
            </n-input>
          </n-form-item>
          <n-form-item label="确认密码" path="confirm_password">
            <n-input
              v-model:value="pwdForm.confirm_password"
              type="password"
              placeholder="请再次输入密码"
              show-password-on="click"
              clearable
            >
              <template #prefix><n-icon><IconLock :size="20" /></n-icon></template>
            </n-input>
          </n-form-item>
          <n-form-item>
            <n-button type="primary" block color="#000000" :loading="pwdLoading" @click="handleChangePwd">
              确认修改并进入系统
            </n-button>
          </n-form-item>
        </n-form>

        <p class="modal-tip">修改成功后将使用新密码登录，请牢记</p>
      </n-card>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  IconUser,
  IconArrowLeft,
  IconIdBadge2,
  IconLock,
  IconSchool
} from '@tabler/icons-vue'
import { login } from '@/api'
import { FormInst, FormRules, useMessage } from 'naive-ui'
import request from '@/utils/request'

const message = useMessage()
const router = useRouter()

const loading = ref(false)
const rememberPassword = ref(false)
const formRef = ref<FormInst | null>(null)

const form = reactive({ student_number: '', password: '' })
const rules: FormRules = {
  student_number: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 首次登录修改密码弹窗
const showChangePwdModal = ref(false)
const pwdLoading = ref(false)
const pwdFormRef = ref<FormInst | null>(null)
const pwdForm = reactive({ new_password: '', confirm_password: '' })
const pwdRules: FormRules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码不能少于6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string) => {
        if (value !== pwdForm.new_password) return new Error('两次输入的密码不一致')
        return true
      },
      trigger: ['blur', 'input']
    }
  ]
}

onMounted(() => {
  const saved = localStorage.getItem('savedStudentNumber')
  const savedPwd = localStorage.getItem('savedPassword')
  if (saved && savedPwd && localStorage.getItem('rememberPassword') === 'true') {
    form.student_number = saved
    form.password = savedPwd
    rememberPassword.value = true
  }
})

const handleLogin = () => {
  formRef.value?.validate(async (errors) => {
    if (errors) return
    loading.value = true
    try {
      const response = await login({
        username: form.student_number,
        password: form.password
      })
      const { access_token, refresh_token, userInfo, is_first_login } = response
      localStorage.setItem('token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('userInfo', JSON.stringify(userInfo))

      if (rememberPassword.value) {
        localStorage.setItem('savedStudentNumber', form.student_number)
        localStorage.setItem('savedPassword', form.password)
        localStorage.setItem('rememberPassword', 'true')
      } else {
        localStorage.removeItem('savedStudentNumber')
        localStorage.removeItem('savedPassword')
        localStorage.removeItem('rememberPassword')
      }

      if (is_first_login) {
        showChangePwdModal.value = true
      } else {
        message.success('登录成功')
        setTimeout(() => router.push('/student/achievement'), 300)
      }
    } catch (e: any) {
      const msg = e?.response?.data?.msg || e.message || '登录失败，请检查学号和密码是否正确'
      message.error(msg)
    } finally {
      loading.value = false
    }
  })
}

const handleChangePwd = () => {
  pwdFormRef.value?.validate(async (errors) => {
    if (errors) return
    pwdLoading.value = true
    try {
      await request.post('/api/v1/auth/change-password', {
        new_password: pwdForm.new_password,
        confirm_password: pwdForm.confirm_password
      })
      message.success('密码修改成功！')
      showChangePwdModal.value = false
      setTimeout(() => router.push('/student/achievement'), 500)
    } catch (e: any) {
      message.error(e.message || '密码修改失败，请重试')
    } finally {
      pwdLoading.value = false
    }
  })
}

const goToHome = () => router.push('/')
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #e6f7ff 0%, #d0e8ff 50%, #c2e0ff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

.back-home {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #1890ff;
  font-size: 14px;
}

.back-icon {
  margin-right: 5px;
}

.login-container {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.platform-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.icon-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 44px;
  height: 44px;
  background-color: #1890ff;
  border-radius: 4px;
  margin-right: 12px;
}

.platform-icon {
  color: white;
}

.platform-header h1 {
  font-size: 28px;
  font-weight: bold;
  color: #1e293b;
  margin: 0;
}

.login-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  text-align: center;
}

.avatar-container {
  margin-bottom: 15px;
}

.login-box h2 {
  font-size: 20px;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 5px 0;
}

.login-tip {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 20px;
}

.login-form {
  width: 100%;
  text-align: left;
}

.input-icon {
  margin: 0 4px;
}

.remember-password {
  display: flex;
  align-items: center;
}

.login-footer {
  margin-top: 15px;
}

.forget-btn {
  font-size: 14px;
  color: #64748b;
}

/* 弹窗样式 */
.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 16px;
  padding: 10px 14px;
  background: #fff7e6;
  border-radius: 6px;
  border-left: 3px solid #fa8c16;
}

.modal-hint {
  font-size: 13px;
  color: #555;
  line-height: 1.5;
}

.modal-title {
  font-size: 18px;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 20px;
  text-align: center;
}

.pwd-form {
  width: 100%;
}

.modal-tip {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin: 8px 0 0;
}
</style>
