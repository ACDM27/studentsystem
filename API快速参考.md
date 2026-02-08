# API快速参考表

## 🔗 基本信息

- **API Base URL**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs`
- **认证方式**: `Bearer Token (JWT)`

---

## 📋 API端点速查表

### 1️⃣ 认证模块

| 端点 | 方法 | 权限 | 功能 |
|------|------|------|------|
| `/api/v1/auth/login` | POST | 公开 | 用户登录 |

---

### 2️⃣ 公共模块

| 端点 | 方法 | 权限 | 功能 |
|------|------|------|------|
| `/api/v1/common/teachers` | GET | 登录用户 | 获取教师列表 |
| `/api/v1/common/upload` | POST | 登录用户 | 文件上传 |

---

### 3️⃣ 学生模块

| 端点 | 方法 | 权限 | 功能 |
|------|------|------|------|
| `/api/v1/student/ocr/recognize` | POST | 学生 | 证书OCR识别（步骤1） |
| `/api/v1/student/achievements` | POST | 学生 | 提交成果（步骤2） |
| `/api/v1/student/achievements` | GET | 学生 | 获取我的成果列表 |
| `/api/v1/student/certificates` | GET | 学生 | 获取我的证书列表 |
| `/api/v1/student/persona` | GET | 学生 | 获取学生画像 |
| `/api/v1/student/ai/chat` | POST | 学生 | AI对话 |

---

### 4️⃣ 管理员模块

| 端点 | 方法 | 权限 | 功能 |
|------|------|------|------|
| `/api/v1/admin/achievements` | GET | 管理员 | 获取成果审核列表 |
| `/api/v1/admin/achievements/{id}/audit` | PATCH | 管理员 | 审核成果 |

---

### 5️⃣ 证书识别模块

| 端点 | 方法 | 权限 | 功能 |
|------|------|------|------|
| `/api/certificate/recognize` | POST | 登录用户 | 独立证书识别 |
| `/api/certificate/batch-recognize` | POST | 登录用户 | 批量证书识别 |
| `/api/certificate/health` | GET | 公开 | 服务健康检查 |

---

### 6️⃣ 系统端点

| 端点 | 方法 | 权限 | 功能 |
|------|------|------|------|
| `/` | GET | 公开 | API信息 |
| `/health` | GET | 公开 | 健康检查 |

---

## 🎨 常用请求示例

### 登录
```javascript
POST /api/v1/auth/login
{
  "username": "student001",
  "password": "password123"
}
```

### 证书识别
```javascript
POST /api/v1/student/ocr/recognize
Content-Type: multipart/form-data
file: [certificate_image.jpg]
```

### 提交成果
```javascript
POST /api/v1/student/achievements
{
  "teacher_id": 1,
  "title": "竞赛一等奖",
  "type": "competition",
  "evidence_url": "/uploads/students/1/certificates/abc.jpg"
}
```

### 审核成果（通过）
```javascript
PATCH /api/v1/admin/achievements/123/audit
{
  "action": "approve",
  "comment": "符合要求"
}
```

### 审核成果（拒绝）
```javascript
PATCH /api/v1/admin/achievements/123/audit
{
  "action": "reject",
  "comment": "证书不清晰"  // 必填
}
```

### AI对话
```javascript
POST /api/v1/student/ai/chat
{
  "session_id": null,  // 新会话传null
  "message": "我想了解如何提升能力"
}
```

---

## 📦 数据字典

### 用户角色 (role)
- `student` - 学生
- `admin` - 管理员

### 成果状态 (status)
- `pending` - 待审核
- `approved` - 已通过
- `rejected` - 已拒绝

### 成果类型 (type)
- `competition` - 学科竞赛
- `paper` - 论文发表
- `patent` - 专利
- `project` - 项目
- `certificate` - 职业证书

### 审核操作 (action)
- `approve` - 通过
- `reject` - 拒绝

---

## ⚡ HTTP状态码

| 状态码 | 含义 | 前端处理 |
|--------|------|----------|
| 200 | 成功 | 正常处理 |
| 400 | 参数错误 | 提示用户检查输入 |
| 401 | 未认证 | 跳转登录页 |
| 403 | 权限不足 | 提示权限不足 |
| 404 | 资源不存在 | 提示未找到 |
| 500 | 服务器错误 | 提示系统错误 |

---

## 🔑 认证Header

所有需要认证的请求都需要携带：

```javascript
headers: {
  'Authorization': `Bearer ${token}`
}
```

---

## 📁 文件URL格式

```
http://localhost:8000/uploads/{相对路径}
```

示例：
```
http://localhost:8000/uploads/students/1/certificates/abc123.jpg
```

---

## 💡 关键流程

### 成果提交流程（学生端）

1. **上传证书** → `POST /api/v1/student/ocr/recognize`
   - 返回：`file_url` + `recognized_data`

2. **确认信息** → 用户可修改AI识别结果

3. **提交成果** → `POST /api/v1/student/achievements`
   - 使用步骤1的`file_url`作为`evidence_url`

### 成果审核流程（管理员端）

1. **获取列表** → `GET /api/v1/admin/achievements?status=pending`

2. **查看详情** → 显示证书图片、学生信息

3. **审核操作** → `PATCH /api/v1/admin/achievements/{id}/audit`
   - 通过：`action=approve`
   - 拒绝：`action=reject` + `comment`（必填）

### AI对话流程

1. **首次对话** → `session_id: null`
   - 返回新的`session_id`

2. **继续对话** → 使用之前返回的`session_id`
   - 后端自动加载历史上下文

---

## 🎯 前端实现要点

### 1. Axios拦截器

```javascript
// 请求拦截：添加Token
config.headers.Authorization = `Bearer ${token}`;

// 响应拦截：处理401
if (status === 401) {
  router.push('/login');
}
```

### 2. 文件完整URL

```javascript
const getFullUrl = (url) => {
  return `${process.env.VUE_APP_API_BASE_URL}${url}`;
};
```

### 3. 状态标签颜色

```javascript
const statusMap = {
  pending: { text: '待审核', type: 'warning' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' }
};
```

---

## ⚠️ 重要提醒

1. **证书上传**：学生端必须使用 `/api/v1/student/ocr/recognize`，不要用 `/api/certificate/recognize`

2. **拒绝必填意见**：管理员拒绝成果时，`comment`字段必填

3. **文件访问权限**：学生只能访问自己的证书

4. **AI功能状态**：
   - ✅ 证书OCR已实现
   - ⚠️ AI对话、学生画像为Mock数据

5. **分页参数**：
   - `page`: 从1开始
   - `page_size`: 最大100

---

## 🔍 调试技巧

1. **使用Swagger**: `http://localhost:8000/docs`
2. **检查健康**: `GET /health`
3. **查看响应结构**: 所有响应都包含 `code`, `msg`, `data`
4. **Token过期**: 默认24小时，可在环境变量中配置

---

**完整文档**: 参见 `前端API协作文档.md`
