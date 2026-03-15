<template>
  <div class="achievement_detail_page">
    <!-- 页面顶部区域 -->
    <div class="header_area">
      <div class="title_info">
        <n-button quaternary @click="go_back">
          <template #icon>
            <IconArrowLeft :size="24" />
          </template>
          返回
        </n-button>
        <h2>成果详情</h2>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading_state">
      <n-spin size="large" />
      <p>加载中...</p>
    </div>

    <template v-else>
      <div v-if="detail && detail.id">
        <!-- 标题与状态 -->
        <n-card class="info_card">
          <div class="title_row">
            <h3>{{ detail.title }}</h3>
            <n-tag :type="status_tag.type" size="medium">{{ status_tag.text }}</n-tag>
          </div>
          <div class="type_badge">
            <n-tag :bordered="false" type="info" size="small">{{ type_label }}</n-tag>
            <span v-if="detail.created_at" class="submit_time">提交于 {{ format_date(detail.created_at) }}</span>
          </div>
        </n-card>

        <!-- 基本信息卡片 -->
        <n-card class="info_card" title="基本信息">
          <div class="info_grid">
            <div class="info_item" v-if="content.date || detail.awardedAt">
              <span class="label">获奖/发表日期</span>
              <span class="value">{{ format_date(content.date || content.publish_date || content.patent_date || detail.awardedAt) }}</span>
            </div>
            <div class="info_item" v-if="content.award">
              <span class="label">奖项</span>
              <span class="value">{{ award_label(content.award) }}</span>
            </div>
            <div class="info_item" v-if="content.level || content.award_level || detail.level">
              <span class="label">成果级别</span>
              <span class="value">{{ level_label(content.level || content.award_level || detail.level) }}</span>
            </div>
            <div class="info_item" v-if="content.tutor_name">
              <span class="label">指导教师</span>
              <span class="value">{{ content.tutor_name }}<template v-if="content.tutor_department">（{{ content.tutor_department }}）</template></span>
            </div>
          </div>
        </n-card>

        <!-- 论文专属信息 -->
        <n-card v-if="detail.type === 'paper'" class="info_card" title="论文信息">
          <div class="info_grid">
            <div class="info_item" v-if="content.journal_name">
              <span class="label">期刊/会议</span>
              <span class="value">{{ content.journal_name }}</span>
            </div>
            <div class="info_item" v-if="content.journal_level">
              <span class="label">期刊级别</span>
              <span class="value">
                <n-tag :type="journal_tag_type(content.journal_level)" size="small">{{ content.journal_level }}</n-tag>
              </span>
            </div>
            <div class="info_item" v-if="content.publish_status">
              <span class="label">发表状态</span>
              <span class="value">{{ publish_status_label(content.publish_status) }}</span>
            </div>
            <div class="info_item" v-if="content.author_order">
              <span class="label">作者排序</span>
              <span class="value">{{ content.author_order }}</span>
            </div>
            <div class="info_item" v-if="content.doi">
              <span class="label">DOI</span>
              <span class="value doi_value">{{ content.doi }}</span>
            </div>
            <div class="info_item" v-if="content.issn">
              <span class="label">ISSN</span>
              <span class="value">{{ content.issn }}</span>
            </div>
          </div>
        </n-card>

        <!-- 专利专属信息 -->
        <n-card v-if="detail.type === 'patent'" class="info_card" title="专利信息">
          <div class="info_grid">
            <div class="info_item" v-if="content.patent_type">
              <span class="label">专利类型</span>
              <span class="value">{{ content.patent_type }}</span>
            </div>
            <div class="info_item" v-if="content.patent_number">
              <span class="label">专利号/登记号</span>
              <span class="value" style="font-family: monospace;">{{ content.patent_number }}</span>
            </div>
            <div class="info_item" v-if="content.patent_status">
              <span class="label">专利状态</span>
              <span class="value">{{ patent_status_label(content.patent_status) }}</span>
            </div>
            <div class="info_item" v-if="content.patent_inventors">
              <span class="label">发明人/著作权人</span>
              <span class="value">{{ content.patent_inventors }}</span>
            </div>
            <div class="info_item" v-if="content.patent_holder">
              <span class="label">专利权人单位</span>
              <span class="value">{{ content.patent_holder }}</span>
            </div>
          </div>
        </n-card>

        <!-- 竞赛/证书专属 - 团队成员 -->
        <n-card v-if="content.team_members && content.team_members.length" class="info_card" title="团队成员">
          <n-space>
            <n-tag v-for="member in content.team_members" :key="member" size="medium">{{ member }}</n-tag>
          </n-space>
        </n-card>

        <!-- 证书/附件展示 -->
        <n-card v-if="detail.evidence_url || attachment_urls.length" class="info_card" title="证明材料">
          <div class="evidence_area">
            <!-- 主证书图片 -->
            <div v-if="detail.evidence_url" class="evidence_main">
              <n-image
                :src="rotated_src || get_file_url(detail.evidence_url)"
                :fallback-src="''"
                object-fit="contain"
                :img-props="{
                  class: 'evidence_img',
                  ...(rotated_src ? {} : { onLoad: on_evidence_load })
                }"
                :on-error="() => { evidence_is_image = false }"
              />
              <div v-if="img_needs_rotate" class="rotate_hint">
                <span>已自动旋转为横向展示</span>
                <n-button text size="tiny" @click="rotated_src = ''; img_needs_rotate = false">恢复原始方向</n-button>
              </div>
              <div v-if="!evidence_is_image" class="file_link">
                <a :href="get_file_url(detail.evidence_url)" target="_blank" class="attachment_link">
                  <IconFile :size="18" /> 查看证明文件
                </a>
              </div>
            </div>
            <!-- 附件列表 -->
            <div v-if="attachment_urls.length" class="attachment_list">
              <p class="attachment_title">附件文件（{{ attachment_urls.length }} 个）</p>
              <div v-for="(url, idx) in attachment_urls" :key="idx" class="attachment_item">
                <a :href="get_file_url(url)" target="_blank" class="attachment_link">
                  <IconFile :size="16" /> 附件 {{ idx + 1 }}
                </a>
              </div>
            </div>
          </div>
        </n-card>

        <!-- 审核信息 -->
        <n-card v-if="detail.audit_comment || detail.status === 'rejected'" class="info_card" title="审核信息">
          <div class="audit_area">
            <div class="info_item">
              <span class="label">审核状态</span>
              <span class="value">
                <n-tag :type="status_tag.type">{{ status_tag.text }}</n-tag>
              </span>
            </div>
            <div class="info_item" v-if="detail.audit_comment">
              <span class="label">审核意见</span>
              <span class="value audit_comment">{{ detail.audit_comment }}</span>
            </div>
          </div>
        </n-card>

      </div>
      <div v-else class="error_state">
        <n-result status="404" title="未找到成果详情" description="请检查成果ID是否正确或联系管理员">
          <template #footer>
            <n-button @click="go_back">返回</n-button>
          </template>
        </n-result>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import {
  IconArrowLeft,
  IconFile
} from '@tabler/icons-vue'
import request from '@/utils/request'
import { getFileUrl } from '@/api'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const achievement_id = route.params.id
const loading = ref(true)
const evidence_is_image = ref(true)
const img_needs_rotate = ref(false)
const rotated_src = ref('')

// 图片加载后检测：竖向图片用 canvas 旋转为横向
const on_evidence_load = (e: Event) => {
  const img = e.target as HTMLImageElement
  if (img.naturalHeight > img.naturalWidth * 1.2) {
    img_needs_rotate.value = true
    // 用 canvas 旋转图片，生成新的横向 dataURL
    try {
      const canvas = document.createElement('canvas')
      canvas.width = img.naturalHeight
      canvas.height = img.naturalWidth
      const ctx = canvas.getContext('2d')!
      ctx.translate(canvas.width / 2, canvas.height / 2)
      ctx.rotate(Math.PI / 2)
      ctx.drawImage(img, -img.naturalWidth / 2, -img.naturalHeight / 2)
      rotated_src.value = canvas.toDataURL('image/jpeg', 0.92)
    } catch (err) {
      console.warn('Canvas 旋转失败（可能跨域）:', err)
    }
  }
}

// 完整的详情数据，保留后端返回的所有字段
const detail = ref<any>(null)

// content_json 快捷访问
const content = computed(() => detail.value?.content_json || {})

// 附件 URL 列表
const attachment_urls = computed(() => {
  const urls = content.value.attachment_urls
  if (Array.isArray(urls)) return urls
  return []
})

// 类型标签
const type_map: Record<string, string> = {
  'competition': '竞赛类', '1': '竞赛类',
  'research': '科研类', '2': '科研类',
  'project': '项目类', '3': '项目类',
  'paper': '论文类', '4': '论文类',
  'patent': '专利类', '5': '专利类',
  'certification': '证书类', '6': '证书类'
}
const type_label = computed(() => type_map[detail.value?.type] || detail.value?.type || '未知类型')

// 状态标签
const status_tag = computed(() => {
  const s = detail.value?.status
  if (s === 'approved') return { type: 'success' as const, text: '已通过' }
  if (s === 'rejected') return { type: 'error' as const, text: '未通过' }
  return { type: 'warning' as const, text: '审核中' }
})

const award_map: Record<string, string> = {
  grandprize: '特等奖', firstprize: '一等奖', secondprize: '二等奖',
  thirdprize: '三等奖', honorablemention: '优秀奖'
}
const award_label = (v: string) => award_map[v] || v

const level_map: Record<string, string> = {
  international: '国家级', national: '国家级',
  provincial: '省部级',
  university: '校级',
  college: '院级'
}
const level_label = (v: string) => level_map[v] || v

const publish_status_map: Record<string, string> = {
  published: '已发表', accepted: '录用待刊', under_review: '在审中'
}
const publish_status_label = (v: string) => publish_status_map[v] || v

const patent_status_map: Record<string, string> = {
  granted: '已授权', accepted: '已受理', under_review: '实审中', published: '已公开'
}
const patent_status_label = (v: string) => patent_status_map[v] || v

const journal_tag_type = (level: string) => {
  if (['SCI', 'EI'].includes(level)) return 'error'
  if (['北大核心', 'CSSCI'].includes(level)) return 'warning'
  return 'default'
}

const format_date = (dateString: string) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return dateString
    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
  } catch { return dateString }
}

const get_file_url = (url: string) => {
  if (!url) return ''
  if (typeof getFileUrl === 'function') return getFileUrl(url)
  if (url.startsWith('http')) return url
  return url
}

const go_back = () => router.back()

const fetch_detail = async () => {
  if (!achievement_id) {
    message.error('成果ID不存在')
    loading.value = false
    return
  }

  loading.value = true
  try {
    const id = Array.isArray(achievement_id) ? achievement_id[0] : achievement_id
    const response: any = await request.get(`/api/v1/student/achievements/${id}`)

    if (response && response.id) {
      detail.value = response
      return
    }

    // 回退：从列表查找
    try {
      const list: any = await request.get('/api/v1/student/achievements')
      const items = Array.isArray(list) ? list : []
      const found = items.find((item: any) => String(item.id) === String(id))
      if (found) {
        detail.value = found
        return
      }
    } catch {}

    message.warning('未找到成果详情')
  } catch (error: any) {
    console.error('获取成果详情失败:', error)
    message.error('获取成果详情失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => fetch_detail())
</script>

<style scoped>
.achievement_detail_page {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.header_area {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  background-color: #f5f7fa;
  padding: 16px 20px;
  border-radius: 8px;
}

.title_info {
  display: flex;
  align-items: center;
}

.title_info h2 {
  margin: 0 0 0 16px;
  font-size: 20px;
}

.loading_state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
}

.loading_state p {
  margin-top: 16px;
  color: #666;
}

.error_state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  min-height: 400px;
}

.info_card {
  margin-bottom: 16px;
}

.title_row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title_row h3 {
  margin: 0;
  font-size: 20px;
  flex: 1;
}

.type_badge {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.submit_time {
  color: #999;
  font-size: 13px;
}

.info_grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px 32px;
}

.info_item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info_item .label {
  color: #999;
  font-size: 13px;
}

.info_item .value {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  word-break: break-all;
}

.doi_value {
  font-family: monospace;
  font-size: 13px !important;
}

.evidence_area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.evidence_main {
  text-align: center;
}

:deep(.evidence_img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  image-orientation: from-image;
}

.rotate_hint {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #999;
  font-size: 12px;
}

.attachment_title {
  margin: 0 0 8px;
  font-size: 14px;
  color: #666;
}

.attachment_list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment_item {
  padding: 8px 12px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #eee;
}

.attachment_link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #1890ff;
  text-decoration: none;
  font-size: 14px;
}

.attachment_link:hover {
  text-decoration: underline;
}

.file_link {
  margin-top: 8px;
}

.audit_area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.audit_comment {
  padding: 12px;
  background: #fef0f0;
  border-radius: 6px;
  color: #f56c6c;
  line-height: 1.6;
}
</style>
