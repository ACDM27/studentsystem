# 学生综合信息服务平台

面向高校的学生综合信息服务系统，提供成果管理、智能证书识别、AI 对话助手、飞书数据同步等功能。

## 项目结构

```
student_system/
├── backend/          # FastAPI 后端服务
├── frontend/         # 学生端前端（Vue 3）
└── admin/            # 管理端前端（Vue 3，独立项目）
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.12 · FastAPI · SQLAlchemy · MySQL |
| 学生端 | Vue 3 · TypeScript · Vite · Naive UI · Element Plus |
| 管理端 | Vue 3 · TypeScript · Vite · Element Plus |
| AI 能力 | 通义千问 VL（证书OCR）· 通义千问（AI对话） |
| 存储 | MySQL 8.0 · 本地文件存储 |

## 功能模块

### 学生端
- **成果管理**：上传成果证书，支持竞赛、专利、论文、科研、项目、荣誉证书等类型
- **智能 OCR 识别**：上传证书图片自动提取标题、获奖人、等级、日期等字段；支持批量上传
- **AI 对话助手**：基于 Qwen 的智能问答，支持成果填报引导
- **个人画像**：数据可视化，展示学生综合成果统计
- **课程 / 作业 / 活动**：课程信息查看与作业提交
- **飞书导入**：从飞书多维表格批量同步成果数据

### 管理端
- **成果审核**：审核学生提交的成果，支持通过/驳回并填写意见
- **数据概览**：成果统计、类型分布等数据看板

## 本地开发

### 环境要求
- Python 3.10+
- Node.js 18+
- MySQL 8.0+

### 后端启动

```bash
cd backend

# 创建虚拟环境并安装依赖
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# 配置环境变量（复制 .env.example 并填写）
cp .env.example .env

# 初始化数据库
python init_db.py

# 启动服务（默认端口 8000）
uvicorn main:app --reload --port 8000
```

**后端环境变量（`.env`）关键字段：**

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/student_system
SECRET_KEY=your_jwt_secret_key

# 通义千问 API（OCR 与对话）
DASHSCOPE_API_KEY=sk-xxxx
QWEN_VL_MODEL=qwen-vl-max
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 学生端前端启动

```bash
cd frontend
npm install
npm run dev
# 默认访问 http://localhost:5173
```

### 管理端前端启动

```bash
cd admin
npm install
npm run dev
# 默认访问 http://localhost:5174
```

## OCR 智能识别

### 支持的证书类型

| 类型 | 说明 |
|------|------|
| `competition` | 学科竞赛、技能大赛获奖证书 |
| `patent` | 发明/实用新型/外观设计专利证书、软件著作权证书 |
| `paper` | 学术论文发表证明 |
| `research` | 科技成果登记证书 |
| `project` | 创新创业项目证书（互联网+、挑战杯等） |
| `certificate` | 荣誉证书、职业资格证书 |

### 识别流程

1. **图片预处理**：EXIF 方向校正 → 自适应纠偏（投影轮廓法，±15°）→ 上采样 → 去噪 → 对比度增强 → 锐化
2. **类型专属 Prompt**：根据用户选择的证书类型调用对应模板，精准提取字段
3. **自动分类兜底**：未选类型时走两阶段识别（先分类再提取）
4. **专利等级推断**：根据登记号格式（ZL/CN 前缀、SR 软著格式）自动推断国家级/省级
5. **标题生成**：只保留核心成果名称，不拼接人名和颁发机构

## 部署

### Docker 构建

各子项目均包含 `Dockerfile`，可单独构建镜像：

```bash
# 后端
cd backend && docker build -t student-system-backend .

# 学生端前端
cd frontend && docker build -t student-system-frontend .

# 管理端前端
cd admin && docker build -t student-system-admin .
```

### Nginx 反向代理

学生端和管理端各自包含 `nginx.conf`，构建后静态资源通过 Nginx 分发，API 请求代理到后端 8000 端口。

## 数据库

数据库 Schema 详见 [`backend/DATABASE_SCHEMA.md`](backend/DATABASE_SCHEMA.md)。

主要数据表：

| 表名 | 说明 |
|------|------|
| `sys_students` | 学生账户 |
| `sys_teachers` | 教师账户 |
| `biz_achievements` | 成果记录（含审核状态） |
| `ai_chat_sessions` | AI 对话会话 |
| `feishu_configs` | 飞书同步配置 |

## 变更记录

详见 [`backend/CHANGELOG.md`](backend/CHANGELOG.md)。
