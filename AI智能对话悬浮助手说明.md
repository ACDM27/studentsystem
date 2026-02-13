# AI智能对话悬浮助手功能说明

## 功能概述

在学生端平台中新增了全局悬浮AI智能助手，提供以下能力：
- ✅ **全局访问**：在学生端所有页面右侧显示悬浮助手入口
- ✅ **真实AI对话**：接入阿里云通义千问大模型，提供智能学习辅导
- ✅ **上下文感知**：结合学生成果数据和历史对话提供个性化建议
- ✅ **便捷交互**：侧边栏式展开/折叠，支持快捷问题和完整对话切换

## 实现方案

### 后端实现（3个文件）

#### 1. `backend/services/ai_chat_service.py` - AI对话服务（新增）
**功能**：
- 封装通义千问OpenAI兼容API调用
- 实现学生上下文格式化（姓名、专业、成果记录）
- 支持历史对话管理（最近10条）
- 提供system prompt配置（AI助手角色定义）

**核心方法**：
```python
ai_chat_service.chat(
    user_message="用户消息",
    student_context={"name": "张三", "achievements": [...]},
    chat_history=[{"role": "user", "content": "..."}],
    temperature=0.7,
    max_tokens=800
)
```

**特性**：
- 错误处理和降级策略
- Token使用统计
- 复用证书识别服务的OpenAI客户端配置

#### 2. `backend/routers/student.py` - AI对话路由（修改）
**修改位置**：第340-442行 `ai_chat` 函数

**改进**：
- ❌ 移除：Mock响应和TODO注释
- ✅ 新增：真实LLM API调用
- ✅ 优化：学生上下文构建（包含最近20条成果）
- ✅ 增强：历史消息格式化（适配LLM API格式）
- ✅ 新增：usage统计返回

**API响应示例**：
```json
{
  "code": 200,
  "data": {
    "session_id": "uuid-string",
    "message": "AI回复内容...",
    "usage": {
      "prompt_tokens": 150,
      "completion_tokens": 200,
      "total_tokens": 350
    }
  }
}
```

#### 3. `backend/config.py` - 配置（已存在，无需修改）
使用的配置项：
- `DASHSCOPE_API_KEY` / `QWEN_API_KEY`：API密钥
- `QWEN_MODEL_NAME`：对话模型名称（默认 qwen-plus）
- `QWEN_BASE_URL`：通义千问OpenAI兼容端点

### 前端实现（3个文件）

#### 1. `frontend/src/components/common/FloatingAiAssistant.vue` - 悬浮助手组件（新增）

**UI设计**：
```
折叠状态：            展开状态：
┌────────┐          ┌─────────────────────┐
│ 🤖 AI  │          │ 🤖 AI学习助手  [跳转][折叠] │
│ 助手   │   -->    ├─────────────────────┤
└────────┘          │ 欢迎消息/对话历史    │
                    │ （最近5条）         │
                    ├─────────────────────┤
                    │ [输入框] [发送]     │
                    ├─────────────────────┤
                    │ 📊学习成果 💡推荐... │
                    └─────────────────────┘
```

**核心功能**：
- **折叠按钮**：右侧固定，渐变紫色背景，脉搏动画
- **对话面板**：380px宽，最多显示最近5条消息
- **快捷问题**：预设3个快捷按钮（学习成果、学习推荐、学情预警）
- **查看完整对话**：跳转到 `portrait-chat` 页面，携带session_id
- **响应式**：移动端全屏显示

**状态管理**：
- `isExpanded`：展开/折叠状态（默认折叠）
- `messages`：消息列表
- `sessionId`：会话ID（跨页面保持对话）
- `isSending`：发送状态

**动画效果**：
- fade-in：消息淡入
- slide-in/out：面板滑入滑出
- pulse：图标脉搏动画

#### 2. `frontend/src/layout/StudentLayout.vue` - 学生端布局（修改）
**修改**：
- 引入 `FloatingAiAssistant` 组件
- 添加到根容器，确保全局可见

**代码**：
```vue
<template>
  <div class="layout-container">
    <student-sidebar class="sidebar" />
    <div class="content">
      <router-view />
    </div>
    <!-- 全局悬浮AI助手 -->
    <FloatingAiAssistant />
  </div>
</template>
```

#### 3. `frontend/src/utils/icons.ts` - 图标导出（修改）
**新增**：
- `IconSend`：发送按钮图标

## 使用流程

### 学生使用流程
1. **登录学生端**
2. **查看右侧悬浮按钮**（紫色渐变，"AI助手"文字）
3. **点击展开对话面板**
4. **输入问题或点击快捷问题**
5. **查看AI回复**（基于个人成果数据的个性化建议）
6. **（可选）点击"查看完整对话"** 跳转到完整chat页面

### 快捷问题示例
- 📊 **学习成果**："请分析我的学习成果"
- 💡 **学习推荐**："为我推荐学习内容"
- ⚠️ **学情预警**："分析我的学情预警"

## 技术特性

### 1. 上下文感知（RAG）
AI助手会自动获取以下学生信息作为上下文：
- 姓名、专业、班级
- 最近20条已通过的成果记录
- 成果统计（总数、通过数、通过率）

### 2. 会话管理
- 后端自动创建和管理session
- 前端保存session_id，跨页面对话
- 历史消息存储在数据库（`ai_chat_messages`表）

### 3. 性能优化
- **Token控制**：
  - 单次最多800 tokens
  - 历史消息限制10条
  - 成果上下文限制20条
- **防抖处理**：发送按钮防止重复点击
- **懒加载**：悬浮面板首次展开才开始初始化

### 4. 错误处理
- **API失败**：显示友好提示"AI助手暂时无法回复"
- **网络超时**：60秒超时（在request配置中）
- **降级策略**：保持对话界面可用，错误不影响其他功能

## API成本估算

以通义千问 qwen-plus 为例（0.008元/1000 tokens）：

单次对话成本估算：
- 系统提示词：~200 tokens
- 学生上下文：~300 tokens（20条成果）
- 历史消息：~400 tokens（10条）
- 用户问题：~50 tokens
- AI回复：~200 tokens
- **总计**：~1150 tokens ≈ 0.009元/次

月成本估算（1000名学生，每人10次对话）：
- 10,000次 × 0.009元 = **90元/月**

## 与现有功能的关系

### 悬浮助手 vs portrait-chat 对比

| 特性 | 悬浮助手 | portrait-chat |
|------|---------|--------------|
| **位置** | 全局悬浮，任意页面 | 需跳转到专门页面 |
| **显示** | 最近5条消息 | 完整对话历史 |
| **功能** | 快速问答 | 完整功能（结构化数据展示） |
| **结构化数据** | ❌ 不展示 | ✅ 学习成果卡片、职业规划等 |
| **定位** | 快捷入口 | 深度对话 |

**协同策略**：
- 悬浮助手用于**快速咨询**
- 复杂分析引导用户**跳转到portrait-chat**
- 两者共享同一个session，对话无缝衔接

## 部署检查清单

### 必需的环境变量
确保 `.env` 文件配置了以下变量：

```bash
# 阿里云通义千问API密钥（二选一）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxx
# 或
QWEN_API_KEY=sk-xxxxxxxxxxxxxx

# 模型配置（可选，有默认值）
QWEN_MODEL_NAME=qwen-plus  # 或 qwen-turbo / qwen-max
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 数据库表
确保已执行迁移，存在以下表：
- `ai_chat_sessions`：会话表
- `ai_chat_messages`：消息记录表
- `sys_students`：学生表
- `biz_achievements`：成果表

### 前端依赖
确保已安装以下依赖：
- `naive-ui`：UI组件库
- `@tabler/icons-vue`：图标库（已添加IconSend）
- `vue-router`：路由管理

## 测试建议

### 后端测试
```bash
# 测试AI对话接口
curl -X POST http://localhost:8000/api/v1/student/ai/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "请分析我的学习成果",
    "session_id": null
  }'
```

### 前端测试
1. **登录学生端账号**
2. **检查右侧是否显示悬浮按钮**
3. **点击展开，测试对话功能**
4. **测试快捷问题按钮**
5. **测试"查看完整对话"跳转**
6. **测试移动端响应式布局**

## 故障排查

### 悬浮助手不显示
- 检查是否已登录学生端
- 检查浏览器控制台是否有导入错误
- 检查 `StudentLayout.vue` 是否正确引入组件

### AI无法回复
- 检查 `.env` 中的API密钥是否正确
- 检查后端日志，确认是否调用了 `ai_chat_service`
- 检查网络连接，通义千问API是否可访问
- 查看返回的error信息

### 对话历史丢失
- 检查 `sessionId` 是否正确保存
- 查看数据库 `ai_chat_sessions` 和 `ai_chat_messages` 表
- 确认session未过期（backend session管理）

## 未来优化方向

1. **流式响应**：支持打字机效果，提升体验
2. **语音输入**：集成Web Speech API
3. **记忆功能**：长期记忆学生偏好
4. **多模态**：支持图片、文件上传分析
5. **推荐系统**：主动推送学习建议
6. **情感分析**：识别学生情绪，提供心理支持

## 相关文件清单

### 后端文件
- ✅ `backend/services/ai_chat_service.py`（新增）
- ✅ `backend/routers/student.py`（修改）
- 📄 `backend/config.py`（已存在）
- 📄 `backend/models.py`（已存在，包含AiChatSession和AiChatMessage）

### 前端文件
- ✅ `frontend/src/components/common/FloatingAiAssistant.vue`（新增）
- ✅ `frontend/src/layout/StudentLayout.vue`（修改）
- ✅ `frontend/src/utils/icons.ts`（修改）
- 📄 `frontend/src/api/index.ts`（已存在，包含chatWithAI函数）
- 📄 `frontend/src/router/student.routes.ts`（已存在）

---

**开发完成时间**：2026-02-13
**开发者**：AI Assistant
**版本**：v1.0
