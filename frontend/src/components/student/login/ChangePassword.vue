<template>
  <div class="change-pwd-page">
    <div class="change-pwd-container">
      <div class="platform-header">
        <div class="icon-box">
          <n-icon size="32" class="platform-icon">
            <IconSchool :size="32" />
          </n-icon>
        </div>
        <h1>学生综合信息服务平台</h1>
      </div>

      <div class="change-pwd-box">
        <div class="step-hint">
          <n-tag type="info" size="small">首次登录</n-tag>
          <span class="step-text">请设置您的登录密码，后续使用学号+密码登录</span>
        </div>

        <h2>设置登录密码</h2>

        <n-form
          class="pwd-form"
          :model="form"
          :rules="rules"
          ref="formRef"
        >
          <n-form-item label="新密码" path="new_password">
            <n-input
              v-model:value="form.new_password"
              type="password"
              placeholder="请设置密码（至少6位）"
              show-password-on="click"
              clearable
            >
              <template #prefix>
                <n-icon><IconLock :size="20" /></n-icon>
              </template>
            </n-input>
          </n-form-item>

          <n-form-item label="确认密码" path="confirm_password">
            <n-input
              v-model:value="form.confirm_password"
              type="password"
              placeholder="请再次输入密码"
              show-password-on="click"
              clearable
            >
              <template #prefix>
                <n-icon><IconLock :size="20" /></n-icon>
              </template>
            </n-input>
          </n-form-item>

          <n-form-item>
            <n-button
              type="primary"
              block
              color="#000000"
              :loading="loading"
              @click="handleSubmit"
            >
              确认设置密码
            </n-button>
          </n-form-item>
        </n-form>

        <p class="tip-text">设置成功后请牢记密码，忘记密码请联系管理员重置</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { IconLock, IconSchool } from '@tabler/icons-vue'
import { FormInst, FormRules, useMessage } from 'naive-ui'
import request from '@/utils/request'

const router = useRouter()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const loading = ref(false)

const form = reactive({
  new_password: '',
  confirm_password: ''
})

const rules: FormRules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码不能少于6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: string) => {
        if (value !== form.new_password) {
          return new Error('两次输入的密码不一致')
        }
        return true
      },
      trigger: ['blur', 'input']
    }
  ]
}

const handleSubmit = () => {
  formRef.value?.validate(async (errors) => {
    if (errors) return
    loading.value = true
    try {
      await request.post('/api/v1/auth/change-password', {
        new_password: form.new_password,
        confirm_password: form.confirm_password
      })
      message.success('密码设置成功！请使用学号和新密码登录')
      // 清除 token，强制重新登录
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('userInfo')
      setTimeout(() => router.push('/student/login'), 1200)
    } catch (e: any) {
      message.error(e.message || '密码设置失败，请重试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.change-pwd-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #e6f7ff 0%, #d0e8ff 50%, #c2e0ff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.change-pwd-container {
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

.change-pwd-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
}

.step-hint {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding: 10px 14px;
  background: #f0f7ff;
  border-radius: 6px;
  border-left: 3px solid #1890ff;
}

.step-text {
  font-size: 13px;
  color: #555;
}

h2 {
  font-size: 20px;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 24px;
  text-align: center;
}

.pwd-form {
  width: 100%;
}

.tip-text {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin: 12px 0 0;
}
</style>
