<template>
  <div class="resume-generator">
    <header class="header">
      <h1>简历生成器</h1>
      <p>创建专业的个人简历，支持多种模板和实时预览</p>
    </header>
    <main class="main-content">
      <div class="left-column">
        <section class="template-selection">
          <h2><span>选择模板</span></h2>
          <p>选择适合的简历模板风格</p>
          <div class="templates">
            <button
              v-for="template in templates"
              :key="template.id"
              :class="['template-btn', { selected: selected_template === template.id }]"
              @click="selectTemplate(template.id)"
            >
              <div class="template-name">{{ template.name }}</div>
              <div class="template-desc">{{ template.description }}</div>
              <div v-if="selected_template === template.id" class="selected-label">已选择</div>
            </button>
          </div>
        </section>
        <section class="basic-info">
          <n-tabs v-model:value="active_tab" type="card" size="small">
            <n-tab-pane name="basic_info" tab="基本信息">
              <h3>基本信息</h3>
              <n-form :model="basic_info" label-width="80">
                <n-form-item label="姓名">
                  <n-input v-model:value="basic_info.user_name" placeholder="请输入姓名" />
                </n-form-item>
                <n-form-item label="学号">
                  <n-input v-model:value="basic_info.student_id" placeholder="请输入学号" />
                </n-form-item>
                <n-form-item label="手机号">
                  <n-input v-model:value="basic_info.phone" placeholder="请输入手机号" />
                </n-form-item>
                <n-form-item label="邮箱">
                  <n-input v-model:value="basic_info.email" placeholder="请输入邮箱" />
                </n-form-item>
                <n-form-item label="地址">
                  <n-input v-model:value="basic_info.address" placeholder="请输入地址" />
                </n-form-item>
                <n-form-item label="求职意向">
                  <n-input
                    type="textarea"
                    v-model:value="basic_info.job_intention"
                    placeholder="请输入求职意向"
                    rows="3"
                  />
                </n-form-item>
              </n-form>
            </n-tab-pane>
            <n-tab-pane name="education" tab="教育背景">
              <div>教育背景填写区域（待实现）</div>
            </n-tab-pane>
            <n-tab-pane name="projects" tab="项目经历">
              <div>项目经历填写区域（待实现）</div>
            </n-tab-pane>
            <n-tab-pane name="skills" tab="技能特长">
              <div>技能特长填写区域（待实现）</div>
            </n-tab-pane>
            <n-tab-pane name="awards" tab="奖项证书">
              <div>奖项证书填写区域（待实现）</div>
            </n-tab-pane>
          </n-tabs>
        </section>
        <section class="action-buttons">
          <n-button type="primary" @click="exportPDF" class="action-btn">
            <template #icon>
              <IconFileDownload :size="24" />
            </template>
            导出PDF
          </n-button>
          <n-button type="info" @click="saveResume" class="action-btn">
            <template #icon>
              <IconDeviceFloppy :size="24" />
            </template>
            保存简历
          </n-button>
        </section>
      </div>
      <div class="right-column">
        <section class="resume-preview">
          <h2><span>简历预览</span></h2>
          <div class="preview-content">
            <div 
              class="preview-header"
              :style="{ 
                backgroundColor: current_theme.theme_color,
                color: '#fff'
              }"
            >
              <h3>{{ basic_info.user_name || "刘在行" }}</h3>
              <p>计算机科学与技术</p>
              <div class="contact-info">
                <span>📞 {{ basic_info.phone || "13800138000" }}</span>
                <span>✉ {{ basic_info.email || "liuxing@example.com" }}</span>
              </div>
            </div>
            <div class="preview-section">
              <h4 :style="{ color: current_theme.theme_color }">求职意向</h4>
              <p>{{ basic_info.job_intention || "寻求软件开发实习机会，希望在技术团队中学习成长，为公司创造价值。" }}</p>
            </div>
            <div class="preview-section">
              <h4 :style="{ color: current_theme.theme_color }">教育背景</h4>
              <div class="education-item">
                <div class="education-header">
                  <strong>某某大学</strong>
                  <span class="education-time">2021.09 - 2025.06</span>
                </div>
                <p>计算机科学与技术专业 | 本科</p>
                <p>主修课程：数据结构、算法设计、数据库系统、软件工程</p>
              </div>
            </div>
            <div class="preview-section">
              <h4 :style="{ color: current_theme.theme_color }">项目经历</h4>
              <div class="project-item">
                <div class="project-header">
                  <strong>学生管理系统</strong>
                  <span class="project-time">2023.03 - 2023.06</span>
                </div>
                <p>基于Vue.js和Spring Boot开发的学生信息管理系统</p>
                <ul>
                  <li>负责前端界面设计和用户交互逻辑实现</li>
                  <li>实现了学生信息的增删改查功能</li>
                  <li>使用Element UI组件库提升用户体验</li>
                </ul>
              </div>
            </div>
            <div class="preview-section">
              <h4 :style="{ color: current_theme.theme_color }">技能特长</h4>
              <div class="skills-grid">
                <div class="skill-item">
                  <span class="skill-name">前端开发</span>
                  <div class="skill-bar">
                    <div 
                      class="skill-progress" 
                      :style="{ backgroundColor: current_theme.theme_color, width: '85%' }"
                    ></div>
                  </div>
                </div>
                <div class="skill-item">
                  <span class="skill-name">后端开发</span>
                  <div class="skill-bar">
                    <div 
                      class="skill-progress" 
                      :style="{ backgroundColor: current_theme.theme_color, width: '75%' }"
                    ></div>
                  </div>
                </div>
                <div class="skill-item">
                  <span class="skill-name">数据库</span>
                  <div class="skill-bar">
                    <div 
                      class="skill-progress" 
                      :style="{ backgroundColor: current_theme.theme_color, width: '70%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 其他预览内容占位 -->
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { NTabs, NTabPane, NForm, NFormItem, NInput, NButton } from "naive-ui";
import { IconFileDownload, IconDeviceFloppy } from "@tabler/icons-vue";

const templates = [
  { 
    id: "modern", 
    name: "现代简约", 
    description: "简洁现代的设计风格，适合互联网行业",
    theme_color: "#409eff",
    bg_color: "#f0f5ff"
  },
  { 
    id: "classic", 
    name: "经典商务", 
    description: "传统商务风格，适合金融、咨询行业",
    theme_color: "#2c3e50",
    bg_color: "#ecf0f1"
  },
  { 
    id: "creative", 
    name: "创意设计", 
    description: "富有创意的设计，适合设计类专业",
    theme_color: "#9b59b6",
    bg_color: "#f8f4fd"
  },
  { 
    id: "academic", 
    name: "学术研究", 
    description: "学术风格，适合学术研究方向",
    theme_color: "#27ae60",
    bg_color: "#f0f9f4"
  }
];

const selected_template = ref("modern");
const active_tab = ref("basic_info");

const basic_info = ref({
  user_name: "",
  student_id: "",
  phone: "",
  email: "",
  address: "",
  job_intention: ""
});

// 计算当前选中模板的主题颜色
const current_theme = computed(() => {
  const template = templates.find(t => t.id === selected_template.value);
  return template || templates[0];
});

function selectTemplate(id: string) {
  selected_template.value = id;
}

function exportPDF() {
  // 导出PDF功能实现（待完成）
  console.log("导出PDF");
}

function saveResume() {
  // 保存简历功能实现（待完成）
  console.log("保存简历");
}
</script>

<style scoped>
.resume-generator {
  padding: 16px;
  font-family: "Microsoft YaHei", sans-serif;
}
.header {
  margin-bottom: 16px;
}
.header h1 {
  font-weight: 700;
  font-size: 24px;
  margin: 0;
}
.header p {
  color: #666;
  font-size: 14px;
  margin: 4px 0 0 0;
}
.main-content {
  display: flex;
  gap: 16px;
}
.left-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 40%;
}
.right-column {
  flex: 1.5;
  width: 60%;
}
.template-selection {
  border: 1px solid #eaeaea;
  border-radius: 6px;
  padding: 16px;
}
.templates {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
}
.template-btn {
  flex: 1 1 45%;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  position: relative;
  background-color: #fff;
  transition: border-color 0.3s;
}
.template-btn:hover {
  border-color: #409eff;
}
.template-btn.selected {
  border-color: #409eff;
  background-color: #f0f5ff;
}
.selected-label {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: #409eff;
  color: #fff;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 12px;
}
.basic-info {
  border: 1px solid #eaeaea;
  border-radius: 6px;
  padding: 16px;
  flex-grow: 1;
  overflow-y: auto;
}
.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  padding: 16px;
  border: 1px solid #eaeaea;
  border-radius: 6px;
  justify-content: center;
}
.action-btn {
  min-width: 120px;
}
.resume-preview {
  border: 1px solid #eaeaea;
  border-radius: 6px;
  padding: 16px;
  overflow-y: auto;
  height: 100%;
  max-height: 800px;
}
.preview-content {
  border: 1px solid #eaeaea;
  border-radius: 6px;
  overflow: hidden;
}
.preview-header {
  color: #fff;
  padding: 16px;
  border-radius: 6px 6px 0 0;
  transition: background-color 0.3s ease;
}
.preview-header h3 {
  margin: 0 0 8px 0;
}
.contact-info span {
  display: inline-block;
  margin-right: 16px;
}
.preview-section {
  margin-top: 16px;
  padding: 0 16px 16px;
}
.preview-section h4 {
  margin-bottom: 8px;
  transition: color 0.3s ease;
  font-weight: 600;
  border-bottom: 2px solid currentColor;
  padding-bottom: 4px;
}

/* 教育背景样式 */
.education-item {
  margin-bottom: 16px;
}
.education-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.education-time {
  color: #666;
  font-size: 14px;
}

/* 项目经历样式 */
.project-item {
  margin-bottom: 16px;
}
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.project-time {
  color: #666;
  font-size: 14px;
}
.project-item ul {
  margin: 8px 0;
  padding-left: 20px;
}
.project-item li {
  margin-bottom: 4px;
  color: #555;
}

/* 技能特长样式 */
.skills-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.skill-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.skill-name {
  min-width: 80px;
  font-weight: 500;
}
.skill-bar {
  flex: 1;
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}
.skill-progress {
  height: 100%;
  border-radius: 4px;
  transition: all 0.3s ease;
}
</style>