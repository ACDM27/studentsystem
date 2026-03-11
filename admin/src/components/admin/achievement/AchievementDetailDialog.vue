<template>
  <el-dialog
    v-model="dialogVisible"
    title="成果详情"
    width="800px"
    :close-on-click-modal="false"
  >
    <div v-if="achievement" class="achievement-detail">
      <!-- 学生信息 -->
      <el-divider content-position="left">
        <span class="section-title">学生信息</span>
      </el-divider>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="学生姓名">
          {{ achievement.student_name }}
        </el-descriptions-item>
        <el-descriptions-item label="学号">
          <el-tag size="small" type="info">{{ achievement.student_number || '-' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="所属专业">
          {{ achievement.student_major || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="行政班级">
          {{ achievement.student_class || '-' }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 成果信息 -->
      <el-divider content-position="left">
        <span class="section-title">成果信息</span>
      </el-divider>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="成果标题" :span="2">
          {{ achievement.title }}
        </el-descriptions-item>
        <el-descriptions-item label="成果类型">
          {{ ACHIEVEMENT_TYPE_TEXT[achievement.type] || achievement.type }}
        </el-descriptions-item>
        <el-descriptions-item label="指导教师">
          {{ achievement.teacher_name }}
        </el-descriptions-item>
        <el-descriptions-item label="提交时间" :span="2">
          {{ formatDateTime(achievement.create_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="审核状态">
          <el-tag :type="STATUS_COLOR[achievement.status]">
            {{ STATUS_TEXT[achievement.status] }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="achievement.audit_comment" label="审核意见" :span="2">
          {{ achievement.audit_comment }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 证书详情 -->
      <el-divider content-position="left">
        <span class="section-title">证书详情</span>
      </el-divider>
      <el-descriptions v-if="achievement.content_json" :column="2" border>
        <el-descriptions-item
          v-if="achievement.content_json.issuing_organization || achievement.content_json.issuer"
          label="颁发单位"
          :span="2"
        >
          {{ achievement.content_json.issuing_organization || achievement.content_json.issuer }}
        </el-descriptions-item>
        
        <el-descriptions-item
          v-if="achievement.content_json.project_name"
          label="所属项目"
          :span="2"
        >
          {{ achievement.content_json.project_name }}
        </el-descriptions-item>

        <el-descriptions-item
          v-if="achievement.content_json.issue_date || achievement.content_json.date"
          label="颁发日期"
        >
          {{ formatDateOnly(achievement.content_json.issue_date || achievement.content_json.date) }}
        </el-descriptions-item>

        <el-descriptions-item
          v-if="achievement.content_json.award || achievement.content_json.award_name"
          label="奖项名称"
        >
          {{ achievement.content_json.award || achievement.content_json.award_name }}
        </el-descriptions-item>
        
        <el-descriptions-item
          v-if="achievement.content_json.award_level || achievement.content_json.level"
          label="获奖等级"
        >
          <el-tag size="small" effect="plain" type="info">
            {{ formatLevel(achievement.content_json.award_level || achievement.content_json.level) }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item
          v-if="achievement.content_json.certificate_number"
          label="证书编号"
        >
          {{ achievement.content_json.certificate_number }}
        </el-descriptions-item>

        <el-descriptions-item
          v-if="achievement.content_json.team_members && achievement.content_json.team_members.length"
          label="团队成员"
          :span="2"
        >
          <div class="team-tags">
            <el-tag 
              v-for="member in achievement.content_json.team_members" 
              :key="member" 
              size="small" 
              class="mr-1"
            >
              {{ member }}
            </el-tag>
          </div>
        </el-descriptions-item>
        
        <el-descriptions-item
          v-if="achievement.content_json.award_description || achievement.content_json.additional_info"
          label="描述/备注"
          :span="2"
        >
          {{ achievement.content_json.award_description || achievement.content_json.additional_info }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 证书图片 -->
      <el-divider content-position="left">
        <span class="section-title">证书图片</span>
      </el-divider>
      <div v-if="achievement.evidence_url" class="certificate-image">
        <el-image
          :src="getImageUrl(achievement.evidence_url)"
          :preview-src-list="[getImageUrl(achievement.evidence_url)]"
          fit="contain"
          style="width: 100%; max-height: 400px"
        >
          <template #error>
            <div class="image-error">
              <el-icon><Picture /></el-icon>
              <span>图片加载失败</span>
            </div>
          </template>
        </el-image>
      </div>
      <el-empty v-else description="无证书图片" />
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button
          v-if="achievement && achievement.status === 'pending'"
          type="success"
          @click="handleAudit"
        >
          审核成果
        </el-button>
      </div>
    </template>
  </el-dialog>

  <!-- 审核弹窗 -->
  <audit-dialog
    v-model="auditDialogVisible"
    :achievement="achievement"
    @success="handleAuditSuccess"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Picture } from '@element-plus/icons-vue'
import type { Achievement } from '@/api/types'
import { getFileUrl } from '@/api'
import {
  STATUS_TEXT,
  STATUS_COLOR,
  ACHIEVEMENT_TYPE_TEXT
} from '@/utils/constants'
import AuditDialog from './AuditDialog.vue'

interface Props {
  modelValue: boolean
  achievement: Achievement | null
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void // 审核成功事件
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const auditDialogVisible = ref(false)

// 双向绑定弹窗显示状态
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

/**
 * 获取完整的图片URL
 */
const getImageUrl = (url: string): string => {
  if (!url) return ''
  // 确保URL格式正确，如果是相对路径则补全
  return getFileUrl(url)
}

/**
 * 格式化日期时间
 */
const formatDateTime = (dateStr?: string): string => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr || '-'
  }
}

/**
 * 仅格式化日期
 */
const formatDateOnly = (dateStr?: string | number): string => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return String(dateStr)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch {
    return String(dateStr)
  }
}

/**
 * 格式化奖项等级文本
 */
const formatLevel = (level?: string): string => {
  if (!level) return '-'
  const levelMap: Record<string, string> = {
    'international': '国家级',
    'provincial': '省部级',
    'university': '校级',
    'college': '院级'
  }
  return levelMap[level] || level
}

/**
 * 处理审核按钮点击
 */
const handleAudit = () => {
  auditDialogVisible.value = true
}

/**
 * 审核成功处理
 */
const handleAuditSuccess = () => {
  auditDialogVisible.value = false
  dialogVisible.value = false
  emit('success') // 通知父组件刷新列表
}

/**
 * 关闭弹窗
 */
const handleClose = () => {
  dialogVisible.value = false
}
</script>

<style scoped>
.achievement-detail {
  padding: 10px 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e2730;
}

.certificate-image {
  text-align: center;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #909399;
}
</style>
