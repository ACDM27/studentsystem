# 学生信息服务平台 - 前端API协作文档

## 📋 文档概述

**项目名称**: Student Information Service Platform  
**后端版本**: v3.0.0  
**API基础URL**: `http://localhost:8000`  
**API文档**: `http://localhost:8000/docs` (Swagger UI)  
**创建日期**: 2026-01-28  

---

## 🏗️ 后端技术栈

- **框架**: FastAPI 
- **数据库**: MySQL 5.7+ (使用 PyMySQL 驱动)
- **ORM**: SQLAlchemy 2.x
- **认证**: JWT (JSON Web Token)
- **AI服务**: 阿里云通义千问 (Qwen)

---

## 📦 核心功能模块

1. **用户认证** - 登录、JWT Token管理
2. **成果管理** - 学生提交成果、管理员审核
3. **证书识别** - AI OCR识别证书信息
4. **AI对话** - 智能导师对话系统
5. **学生画像** - AI生成的学生能力画像
6. **文件管理** - 文件上传、存储管理

---

## 🔐 认证机制

### Token使用方式

所有需要认证的API请求，都需要在HTTP Header中携带JWT Token：

```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### Token有效期
- **默认有效期**: 1440分钟（24小时）
- **过期处理**: 返回401状态码，前端需跳转登录页

---

## 📡 API响应格式

### 标准响应结构

所有API响应都遵循统一格式：

```json
{
  "code": 200,           // 状态码: 200成功, 400/401/403/404/500错误
  "msg": "success",      // 消息描述
  "data": {}             // 具体数据（根据接口不同而变化）
}
```

### 响应状态码

| 状态码 | 含义 | 处理建议 |
|--------|------|----------|
| `200` | 成功 | 正常处理数据 |
| `400` | 请求参数错误 | 检查请求参数 |
| `401` | 未认证或Token过期 | 跳转到登录页 |
| `403` | 权限不足 | 提示用户权限不足 |
| `404` | 资源不存在 | 提示资源未找到 |
| `500` | 服务器错误 | 提示系统错误，联系管理员 |

---

## 🔌 API端点详情

## 1. 认证模块 (Authentication)

### 1.1 用户登录

**端点**: `POST /api/v1/auth/login`  
**权限**: 无需认证  
**描述**: 用户登录，获取JWT Token

**请求体**:
```json
{
  "username": "student001",
  "password": "password123"
}
```

**成功响应** (code: 200):
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userInfo": {
      "id": 1,
      "name": "张三",           // 学生显示真实姓名，管理员显示用户名
      "role": "student"          // 角色: "student" 或 "admin"
    }
  }
}
```

**失败响应** (code: 401):
```json
{
  "code": 401,
  "msg": "Invalid username or password",
  "data": null
}
```

**前端处理建议**:
1. 登录成功后，保存token到localStorage/sessionStorage
2. 保存userInfo到Vuex/Pinia状态管理
3. 根据role路由到不同页面 (student → 学生端, admin → 管理端)

---

## 2. 公共模块 (Common)

### 2.1 获取教师列表

**端点**: `GET /api/v1/common/teachers`  
**权限**: 需要登录 (学生/管理员均可)  
**描述**: 获取所有教师列表，用于下拉选择

**请求参数**: 无

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": 1,
      "name": "李教授",
      "department": "计算机学院"
    },
    {
      "id": 2,
      "name": "王讲师",
      "department": "软件学院"
    }
  ]
}
```

**前端使用场景**:
- 学生提交成果时，选择指导教师
- 建议在成果提交页面初始化时调用

---

### 2.2 文件上传

**端点**: `POST /api/v1/common/upload`  
**权限**: 需要登录  
**描述**: 上传文件到服务器（通用上传，非证书识别）

**请求体**: `multipart/form-data`
```javascript
const formData = new FormData();
formData.append('file', fileObject);
```

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "url": "/uploads/a1b2c3d4-e5f6-7890.jpg"
  }
}
```

**失败响应** (文件过大):
```json
{
  "code": 400,
  "msg": "File size exceeds maximum limit",
  "data": null
}
```

**限制**:
- 最大文件大小: 10MB
- 支持格式: 由应用层决定

---

## 3. 学生端模块 (Student)

### 3.1 证书OCR识别（步骤1/2）

**端点**: `POST /api/v1/student/ocr/recognize`  
**权限**: 仅学生  
**描述**: 上传证书图片，AI自动识别并返回结构化数据

**请求体**: `multipart/form-data`
```javascript
const formData = new FormData();
formData.append('file', certificateFile);
```

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "recognized_data": {
      // 基础字段
      "title": "全国大学生数学建模竞赛一等奖",
      "date": "2023-12-01",
      "issuer": "中国工业与应用数学学会",
      "suggested_type": "学科竞赛",
      "award_level": "国家级一等奖",
      "certificate_number": "CUMCM2023-A-001",
      "recipient_name": "张三",
      
      // 增强字段
      "project_name": "基于AI的智能推荐系统",
      "team_members": ["张三", "李四", "王五"],
      "advisors": ["李教授"],
      "additional_info": "团队项目",
      
      // 置信度分数
      "recognition_confidence": {
        "overall": 0.95,
        "title": 0.98,
        "date": 0.92
      }
    },
    
    "file_url": "/uploads/students/1/certificates/abc123.jpg",
    
    "file_info": {
      "filename": "abc123.jpg",
      "original_filename": "certificate.jpg",
      "size_bytes": 524288
    },
    
    "ai_metadata": {
      "model_used": "qwen-vl-max",
      "recognition_time": "2026-01-28T01:10:00Z",
      "confidence": "high"
    },
    
    "usage": {
      "input_tokens": 1500,
      "output_tokens": 300
    }
  }
}
```

**失败响应** (识别失败但文件已保存):
```json
{
  "code": 500,
  "msg": "Certificate saved but recognition failed: AI service timeout",
  "data": {
    "file_url": "/uploads/students/1/certificates/abc123.jpg",
    "recognized_data": null
  }
}
```

**前端处理建议**:
1. 显示识别结果供用户确认
2. 用户可以手动修改AI识别的内容
3. **重要**: 保存`file_url`，在步骤2提交成果时使用
4. 如果识别失败，文件仍然保存，可以让用户手动填写信息

---

### 3.2 提交成果（步骤2/2）

**端点**: `POST /api/v1/student/achievements`  
**权限**: 仅学生  
**描述**: 确认并提交成果记录

**请求体**:
```json
{
  "teacher_id": 1,
  "title": "全国大学生数学建模竞赛一等奖",
  "type": "competition",
  "content_json": {
    "certificate_name": "全国大学生数学建模竞赛一等奖",
    "issuing_organization": "中国工业与应用数学学会",
    "issue_date": "2023-12-01",
    "award_level": "国家级一等奖"
  },
  "evidence_url": "/uploads/students/1/certificates/abc123.jpg"
}
```

**字段说明**:
- `teacher_id`: 必填，指导教师ID（从教师列表获取）
- `title`: 必填，成果标题
- `type`: 必填，成果类型（见下方类型列表）
- `content_json`: 可选，详细信息（建议直接使用OCR识别结果）
- `evidence_url`: 可选，证书文件URL（来自步骤1的返回值）

**成果类型 (type字段)**:
- `competition`: 学科竞赛
- `paper`: 论文发表
- `patent`: 专利
- `project`: 项目
- `certificate`: 职业证书

**成功响应**:
```json
{
  "code": 200,
  "msg": "Achievement submitted successfully",
  "data": {
    "id": 123
  }
}
```

**失败响应示例**:

1. 教师不存在 (404):
```json
{
  "code": 404,
  "msg": "Teacher not found",
  "data": null
}
```

2. 证书访问权限不足 (403):
```json
{
  "code": 403,
  "msg": "Access denied: You can only use your own certificates",
  "data": null
}
```

---

### 3.3 获取我的成果列表

**端点**: `GET /api/v1/student/achievements`  
**权限**: 仅学生  
**描述**: 查询当前学生的所有成果

**请求参数**:
- `status` (可选): 过滤状态 - `pending`/`approved`/`rejected`

**示例请求**:
```
GET /api/v1/student/achievements?status=pending
```

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": 1,
      "title": "全国大学生数学建模竞赛一等奖",
      "type": "competition",
      "content_json": {
        "certificate_name": "全国大学生数学建模竞赛一等奖",
        "issue_date": "2023-12-01"
      },
      "evidence_url": "/uploads/students/1/certificates/abc123.jpg",
      "status": "pending",          // pending/approved/rejected
      "audit_comment": null,        // 审核意见（拒绝时必有）
      "created_at": "2026-01-28T01:10:00",
      "teacher_name": "李教授"
    }
  ]
}
```

**状态说明**:
- `pending`: 待审核（黄色标签）
- `approved`: 已通过（绿色标签）
- `rejected`: 已拒绝（红色标签，显示audit_comment）

---

### 3.4 获取我的证书列表

**端点**: `GET /api/v1/student/certificates`  
**权限**: 仅学生  
**描述**: 获取已上传的所有证书文件

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "certificates": [
      {
        "filename": "abc123.jpg",
        "original_filename": "certificate.jpg",
        "url": "/uploads/students/1/certificates/abc123.jpg",
        "size_bytes": 524288,
        "uploaded_at": "2026-01-28T01:10:00"
      }
    ],
    "total": 1
  }
}
```

**前端使用场景**:
- 证书管理页面
- 可以展示缩略图，点击查看大图

---

### 3.5 获取学生画像

**端点**: `GET /api/v1/student/persona`  
**权限**: 仅学生  
**描述**: 获取AI生成的学生能力画像

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "strengths": ["数学建模", "创新能力"],
    "achievements_summary": "参与多项竞赛并获奖",
    "suggested_improvements": ["加强英语能力", "拓展跨学科知识"],
    "generated_at": "2026-01-28T01:10:00Z"
  }
}
```

**注意事项**:
- 画像数据缓存7天
- 当有新成果被审核通过时，缓存自动失效，下次请求会重新生成
- **TODO**: 当前返回mock数据，后续会接入真实LLM生成

---

### 3.6 AI对话

**端点**: `POST /api/v1/student/ai/chat`  
**权限**: 仅学生  
**描述**: 与AI导师进行对话，支持上下文记忆

**请求体**:

1. 新建会话:
```json
{
  "session_id": null,
  "message": "我想了解如何提升数学建模能力"
}
```

2. 继续会话:
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "有什么具体的学习资源推荐吗？"
}
```

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "根据你的成果记录，我看到你在学科竞赛有不错的表现。关于你的问题：我想了解如何提升数学建模能力，我建议..."
  }
}
```

**前端处理建议**:
1. 首次对话，`session_id`传null
2. 收到响应后，保存`session_id`到组件状态
3. 后续对话都带上这个`session_id`
4. AI会根据学生的成果记录提供个性化建议

**会话管理**:
- 会话ID为UUID格式
- 后端自动保存所有对话历史
- 后端会检索最近10条消息作为上下文
- 后端会自动加载学生的已审核成果作为RAG上下文

**TODO**: 当前AI响应为mock数据，后续会接入真实LLM API

---

## 4. 管理员模块 (Admin)

### 4.1 获取待审核成果列表

**端点**: `GET /api/v1/admin/achievements`  
**权限**: 仅管理员  
**描述**: 获取所有成果记录，支持筛选和分页

**请求参数**:
- `status` (可选): 状态筛选 - `pending`/`approved`/`rejected`
- `student_name` (可选): 学生姓名模糊搜索
- `page` (默认1): 页码
- `page_size` (默认10): 每页数量（最大100）

**示例请求**:
```
GET /api/v1/admin/achievements?status=pending&page=1&page_size=10
```

**成功响应**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "全国大学生数学建模竞赛一等奖",
        "type": "competition",
        "student_name": "张三",
        "teacher_name": "李教授",
        "evidence_url": "/uploads/students/1/certificates/abc123.jpg",
        "status": "pending",
        "audit_comment": null,
        "create_time": "2026-01-28T01:10:00",
        "content_json": {
          "certificate_name": "全国大学生数学建模竞赛一等奖",
          "issue_date": "2023-12-01"
        }
      }
    ],
    "total": 25
  }
}
```

**前端处理建议**:
1. 使用el-table或类似组件展示
2. 实现分页组件
3. 添加状态筛选器
4. 添加学生姓名搜索框

---

### 4.2 审核成果

**端点**: `PATCH /api/v1/admin/achievements/{achievement_id}/audit`  
**权限**: 仅管理员  
**描述**: 审核成果（通过或拒绝）

**路径参数**:
- `achievement_id`: 成果ID

**请求体**:

1. 通过:
```json
{
  "action": "approve",
  "comment": "优秀成果，符合要求"  // 可选
}
```

2. 拒绝:
```json
{
  "action": "reject",
  "comment": "证书不清晰，请重新上传"  // 拒绝时必填
}
```

**成功响应**:
```json
{
  "code": 200,
  "msg": "Achievement approved successfully",
  "data": null
}
```

**失败响应**:

1. 成果不存在 (404):
```json
{
  "code": 404,
  "msg": "Achievement not found",
  "data": null
}
```

2. 拒绝时未填写意见 (400):
```json
{
  "code": 400,
  "msg": "Comment is required for rejection",
  "data": null
}
```

**副作用**:
- 审核通过后，学生的画像缓存会自动失效，下次访问会重新生成

---

## 5. 证书识别模块 (Certificate Recognition)

### 5.1 证书识别（独立服务）

**端点**: `POST /api/certificate/recognize`  
**权限**: 需要登录  
**描述**: 独立的证书识别服务，不保存到数据库

**请求体**: `multipart/form-data`

**成功响应**:
```json
{
  "success": true,
  "data": {
    "certificate_name": "全国大学生数学建模竞赛一等奖",
    "recipient_name": "张三",
    "issuing_organization": "中国工业与应用数学学会",
    "issue_date": "2023-12-01",
    "certificate_number": "CUMCM2023-A-001",
    "award_level": "国家级一等奖",
    "category": "学科竞赛",
    "additional_info": "团队成员：张三、李四、王五",
    "recognition_time": "2026-01-28T01:10:00Z",
    "model_used": "qwen-vl-max",
    "confidence": "high"
  }
}
```

**与学生端OCR的区别**:
- 这个接口不保存文件，仅用于临时识别
- 学生端的`/api/v1/student/ocr/recognize`会永久保存证书
- 建议学生端始终使用`/api/v1/student/ocr/recognize`

---

### 5.2 批量证书识别

**端点**: `POST /api/certificate/batch-recognize`  
**权限**: 需要登录  
**描述**: 批量识别多个证书

**限制**: 最多10个文件

**成功响应**:
```json
{
  "success": true,
  "results": [
    {
      "filename": "cert1.jpg",
      "success": true,
      "data": { /* 识别数据 */ }
    },
    {
      "filename": "cert2.jpg",
      "success": false,
      "error": "Invalid file type"
    }
  ],
  "total": 2,
  "successful": 1,
  "failed": 1
}
```

---

### 5.3 服务健康检查

**端点**: `GET /api/certificate/health`  
**权限**: 无需认证  
**描述**: 检查证书识别服务状态

**成功响应**:
```json
{
  "status": "ready",
  "configured": true,
  "model": "qwen-vl-max",
  "message": "Certificate recognition service is ready"
}
```

---

## 6. 系统端点

### 6.1 API根路径

**端点**: `GET /`  
**权限**: 无需认证  
**描述**: API信息

**响应**:
```json
{
  "message": "Student Information Service Platform API",
  "version": "3.0.0",
  "docs": "/docs"
}
```

---

### 6.2 健康检查

**端点**: `GET /health`  
**权限**: 无需认证  
**描述**: 系统健康检查

**响应**:
```json
{
  "status": "healthy"
}
```

---

## 📂 静态文件访问

### 文件URL格式

所有上传的文件都可以通过以下方式访问：

```
http://localhost:8000/uploads/{相对路径}
```

**示例**:
```
http://localhost:8000/uploads/students/1/certificates/abc123.jpg
```

**访问控制**:
- 学生只能访问自己的证书 (`/uploads/students/{student_id}/`)
- 管理员可以访问所有文件
- 由`CertificateAccessMiddleware`中间件控制

---

## 🗄️ 数据库模型

### 用户角色 (UserRole)
- `student`: 学生
- `admin`: 管理员

### 成果状态 (AchievementStatus)
- `pending`: 待审核
- `approved`: 已通过
- `rejected`: 已拒绝

### 消息角色 (MessageRole)
- `user`: 用户消息
- `assistant`: AI助手消息

### 成果类型建议
- `competition`: 学科竞赛
- `paper`: 论文发表
- `patent`: 专利
- `project`: 项目
- `certificate`: 职业证书

---

## 🔧 环境配置

### 必需的环境变量

后端在`.env`文件中配置，前端需要了解：

```env
# 数据库
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/student_system

# JWT密钥
SECRET_KEY=your-secret-key-change-this-in-production

# 文件上传
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# AI服务（通义千问）
QWEN_API_KEY=sk-xxx
QWEN_MODEL_NAME=qwen-plus
QWEN_VL_MODEL=qwen-vl-max
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# CORS允许的源
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

**前端需要配置的环境变量**:
```env
VUE_APP_API_BASE_URL=http://localhost:8000
```

---

## 🚀 前端开发建议

### 1. API请求封装

推荐使用axios + 拦截器统一处理：

```javascript
// api/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000
});

// 请求拦截器 - 添加Token
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器 - 统一处理错误
instance.interceptors.response.use(
  response => {
    const { code, msg, data } = response.data;
    if (code === 200) {
      return data;  // 直接返回data部分
    } else {
      // 业务错误
      ElMessage.error(msg);
      return Promise.reject(new Error(msg));
    }
  },
  error => {
    if (error.response?.status === 401) {
      // Token过期，跳转登录
      localStorage.removeItem('token');
      router.push('/login');
    } else {
      ElMessage.error(error.message || '请求失败');
    }
    return Promise.reject(error);
  }
);

export default instance;
```

---

### 2. API模块化

```javascript
// api/auth.js
import axios from './axios';

export const login = (username, password) => {
  return axios.post('/api/v1/auth/login', { username, password });
};
```

```javascript
// api/student.js
import axios from './axios';

export const recognizeCertificate = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return axios.post('/api/v1/student/ocr/recognize', formData);
};

export const submitAchievement = (data) => {
  return axios.post('/api/v1/student/achievements', data);
};

export const getMyAchievements = (status = null) => {
  return axios.get('/api/v1/student/achievements', {
    params: status ? { status } : {}
  });
};

export const chatWithAI = (sessionId, message) => {
  return axios.post('/api/v1/student/ai/chat', {
    session_id: sessionId,
    message
  });
};
```

```javascript
// api/admin.js
import axios from './axios';

export const getAchievementsForReview = (params) => {
  return axios.get('/api/v1/admin/achievements', { params });
};

export const auditAchievement = (achievementId, action, comment) => {
  return axios.patch(`/api/v1/admin/achievements/${achievementId}/audit`, {
    action,
    comment
  });
};
```

---

### 3. 状态管理示例 (Pinia)

```javascript
// stores/user.js
import { defineStore } from 'pinia';
import { login } from '@/api/auth';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null')
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.userInfo?.role === 'admin',
    isStudent: (state) => state.userInfo?.role === 'student'
  },
  
  actions: {
    async login(username, password) {
      const data = await login(username, password);
      this.token = data.token;
      this.userInfo = data.userInfo;
      
      localStorage.setItem('token', data.token);
      localStorage.setItem('userInfo', JSON.stringify(data.userInfo));
    },
    
    logout() {
      this.token = '';
      this.userInfo = null;
      localStorage.removeItem('token');
      localStorage.removeItem('userInfo');
    }
  }
});
```

---

### 4. 文件预览处理

```javascript
// 图片完整URL
const getImageUrl = (relativeUrl) => {
  if (!relativeUrl) return '';
  return `${process.env.VUE_APP_API_BASE_URL}${relativeUrl}`;
};

// 在模板中使用
<el-image 
  :src="getImageUrl(achievement.evidence_url)" 
  :preview-src-list="[getImageUrl(achievement.evidence_url)]"
/>
```

---

### 5. 路由权限控制

```javascript
// router/index.js
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login');
  } else if (to.meta.role && userStore.userInfo?.role !== to.meta.role) {
    next('/403');  // 权限不足
  } else {
    next();
  }
});

// 路由配置
const routes = [
  {
    path: '/student',
    meta: { requiresAuth: true, role: 'student' },
    children: [...]
  },
  {
    path: '/admin',
    meta: { requiresAuth: true, role: 'admin' },
    children: [...]
  }
];
```

---

## ⚠️ 注意事项

### 1. 证书上传流程

**推荐流程**（两步式）:
1. 调用 `/api/v1/student/ocr/recognize` 上传证书
2. 展示AI识别结果供用户确认/修改
3. 用户点击"确认提交"，调用 `/api/v1/student/achievements`

**重要**: 
- 必须保存步骤1返回的`file_url`
- 步骤2的`evidence_url`字段必须使用步骤1返回的`file_url`
- 不要使用 `/api/certificate/recognize`，它不会保存文件

---

### 2. 文件访问权限

- 学生端显示证书时，URL必须是完整路径
- 后端会验证学生只能访问自己的证书
- 管理员可以查看所有证书

---

### 3. AI功能状态

当前AI功能状态：

| 功能 | 状态 | 说明 |
|------|------|------|
| 证书OCR识别 | ✅ 已实现 | 使用qwen-vl-max模型 |
| AI对话 | ⚠️ Mock数据 | 框架已完成，需配置LLM API |
| 学生画像生成 | ⚠️ Mock数据 | 框架已完成，需配置LLM API |

---

### 4. 错误处理

建议前端统一处理这些场景：

```javascript
try {
  const data = await submitAchievement(formData);
  ElMessage.success('提交成功');
} catch (error) {
  // axios拦截器已处理通用错误
  // 这里只需处理特殊业务逻辑
  if (error.message.includes('Teacher not found')) {
    ElMessage.error('请选择有效的指导教师');
  }
}
```

---

### 5. 分页处理建议

```javascript
// 管理员成果列表组件
const pagination = ref({
  page: 1,
  page_size: 10,
  total: 0
});

const loadAchievements = async () => {
  const data = await getAchievementsForReview({
    page: pagination.value.page,
    page_size: pagination.value.page_size,
    status: selectedStatus.value
  });
  
  achievements.value = data.list;
  pagination.value.total = data.total;
};
```

---

## 📞 技术支持

### API调试工具

**Swagger UI**: `http://localhost:8000/docs`
- 可以直接在浏览器中测试所有API
- 自动生成请求示例
- 可以快速验证Token是否有效

### 常见问题

1. **Q: Token过期怎么办？**
   - A: 前端检测到401状态码后，清除本地token并跳转登录页

2. **Q: 如何区分AI识别失败和服务错误？**
   - A: 识别失败返回code 500且msg包含"recognition failed"，但仍返回file_url

3. **Q: 管理员能否查看学生的AI对话？**
   - A: 当前API未提供此功能，如需要可联系后端添加

4. **Q: 文件大小限制是多少？**
   - A: 默认10MB，超过会返回400错误

---

## 📝 更新日志

### v3.0.0 (2026-01-28)
- ✅ 完整的用户认证系统
- ✅ 成果管理（提交、审核）
- ✅ 证书OCR识别（qwen-vl-max）
- ✅ AI对话框架（待接入LLM）
- ✅ 学生画像框架（待接入LLM）
- ✅ 文件访问权限控制
- ✅ RESTful API设计
- ✅ Swagger API文档

---

## 📚 相关文档

- **数据库Schema**: `backend/DATABASE_SCHEMA.md`
- **后端README**: `backend/README.md`
- **Swagger文档**: `http://localhost:8000/docs`

---

**文档维护者**: Antigravity AI  
**最后更新**: 2026-01-28
