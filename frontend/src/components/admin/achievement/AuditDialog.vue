<template>
  <el-dialog
    v-model="dialogVisible"
    title="审核成果"
    width="600px"
    :close-on-click-modal="false"
  >
    <div v-if="achievement" class="audit-content">
      <!-- 成果基本信息 -->
      <el-alert
        :title="`成果标题：${achievement.title}`"
        type="info"
        :closable="false"
        show-icon
      />

      <el-form
        ref="auditFormRef"
        :model="auditForm"
        :rules="auditRules"
        label-width="100px"
        class="audit-form"
      >
        <el-form-item label="审核操作" prop="action">
          <el-radio-group v-model="auditForm.action">
            <el-radio label="approve">批准通过</el-radio>
            <el-radio label="reject">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="审核意见" prop="comment">
          <el-input
            v-model="auditForm.comment"
            type="textarea"
            :rows="4"
            :placeholder="computedPlaceholder"
          />
        </el-form-item>
      </el-form>

      <el-divider />

      <el-alert
        v-if="auditForm.action === 'approve'"
        title="批准后，该成果将被标记为已通过，学生可在个人主页查看。"
        type="success"
        :closable="false"
      />
      <el-alert
        v-else
        title="拒绝后，该成果将被标记为已拒绝，学生将收到拒绝原因。"
        type="warning"
        :closable="false"
      />
    </div>

    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button
        type="primary"
        :loading="submitting"
        @click="handleSubmit"
      >
        确认提交
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { auditAchievement } from '@/api'
import type { Achievement } from '@/api/types'

interface Props {
  modelValue: boolean
  achievement: Achievement | null
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 双向绑定弹窗显示状态
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 审核表单
const auditFormRef = ref<FormInstance>()
const auditForm = reactive({
  action: 'approve' as 'approve' | 'reject',
  comment: ''
})

// 表单验证规则
const auditRules: FormRules = {
  action: [
    { required: true, message: '请选择审核操作', trigger: 'change' }
  ],
  comment: [
    {
      validator: (rule, value, callback) => {
        if (auditForm.action === 'reject' && !value) {
          callback(new Error('拒绝时必须填写原因'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const submitting = ref(false)

// 计算placeholder
const computedPlaceholder = computed(() => {
  return auditForm.action === 'reject' ? '拒绝时必须填写原因' : '选填，可以填写审核意见'
})

/**
 * 监听弹窗打开，重置表单
 */
watch(dialogVisible, (visible) => {
  if (visible) {
    auditForm.action = 'approve'
    auditForm.comment = ''
    auditFormRef.value?.clearValidate()
  }
})

/**
 * 提交审核
 */
const handleSubmit = async () => {
  if (!auditFormRef.value || !props.achievement) return

  // 验证表单
  const valid = await auditFormRef.value.validate().catch(() => false)
  if (!valid) return

  // 确认提示
  const actionText = auditForm.action === 'approve' ? '批准' : '拒绝'
  try {
    await ElMessageBox.confirm(
      `确定要${actionText}该成果吗？`,
      '确认提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
  } catch {
    return
  }

  // 提交审核
  submitting.value = true
  try {
    await auditAchievement(props.achievement.id, {
      action: auditForm.action,
      comment: auditForm.comment || undefined
    })

    ElMessage.success('审核成功')
    dialogVisible.value = false
    emit('success')
  } catch (error: any) {
    console.error('审核失败:', error)
    ElMessage.error(error.message || '审核失败，请重试')
  } finally {
    submitting.value = false
  }
}

/**
 * 取消审核
 */
const handleCancel = () => {
  dialogVisible.value = false
}
</script>

<style scoped>
.audit-content {
  padding: 10px 0;
}

.audit-form {
  margin-top: 20px;
}
</style>
