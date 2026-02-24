# 学生综合信息服务平台 - 项目结构

## 项目概述
学生综合信息服务平台，基于 FastAPI 构建的后端服务，提供学生信息管理、荣誉管理、师生关系管理和AI智能分析等功能。

## 目录结构

```
student_system/
├── .git/                      # Git版本控制
├── .venv/                     # Python虚拟环境（不提交）
├── backend/                   # 后端服务
│   ├── routers/              # API路由模块
│   │   ├── admin.py         # 管理员API
│   │   ├── auth.py          # 认证API
│   │   ├── common.py        # 公共API
│   │   ├── debate.py        # 辩论赛API
│   │   ├── student.py       # 学生API
│   │   └── ocr.py           # OCR识别API
│   ├── services/            # 业务逻辑层
│   │   ├── ai_service.py    # AI服务
│   │   ├── auth_service.py  # 认证服务
│   │   ├── ocr_service.py   # OCR服务
│   │   ├── student_service.py # 学生服务
│   │   └── system_state.py  # 系统状态服务
│   ├── middleware/          # 中间件
│   │   ├── cors.py         # CORS配置
│   │   └── logging.py      # 日志中间件
│   ├── main.py             # FastAPI应用入口
│   ├── config.py           # 应用配置
│   ├── database.py         # 数据库连接
│   ├── models.py           # SQLAlchemy ORM模型
│   ├── schemas.py          # Pydantic数据验证模型
│   ├── auth.py             # JWT认证逻辑
│   ├── dependencies.py     # 依赖注入
│   ├── utils.py            # 工具函数
│   ├── init_db.py          # 数据库初始化脚本
│   ├── quickstart.ps1      # 快速启动脚本
│   ├── requirements.txt    # Python依赖
│   ├── .env                # 环境变量（不提交）
│   ├── .env.example        # 环境变量示例
│   ├── .gitignore          # Git忽略配置
│   ├── README.md           # 项目说明
│   ├── DATABASE_SCHEMA.md  # 数据库架构文档
│   └── CLEANUP_REPORT.md   # 清理报告
├── .gitignore              # 根目录Git忽略配置
├── rule.txt                # 项目规则
└── PROJECT_STRUCTURE.md    # 本文档

```

## 核心文件说明

### 应用入口
- **`main.py`**: FastAPI应用主文件，定义应用实例、中间件、路由注册

### 配置与环境
- **`config.py`**: 应用配置类，从环境变量读取配置
- **`.env`**: 环境变量文件（包含敏感信息，不提交到版本控制）
- **`.env.example`**: 环境变量模板，供开发者参考

### 数据层
- **`database.py`**: 数据库连接管理，SQLAlchemy引擎和会话配置
- **`models.py`**: ORM模型定义（User, Achievement, TeacherRelation, Contest等）
- **`schemas.py`**: Pydantic模型，用于API请求/响应数据验证
- **`init_db.py`**: 数据库表初始化脚本

### 认证与安全
- **`auth.py`**: JWT token生成和验证
- **`dependencies.py`**: FastAPI依赖注入，包括用户认证、权限检查等

### 业务逻辑
- **`services/`**: 服务层，包含核心业务逻辑
  - `ai_service.py`: 阿里云百炼AI集成
  - `auth_service.py`: 用户认证与授权
  - `ocr_service.py`: 证书OCR识别
  - `student_service.py`: 学生信息管理
  - `system_state.py`: 系统状态管理（辩论赛等）

### API路由
- **`routers/`**: API端点定义
  - `auth.py`: 登录、注册、密码管理
  - `student.py`: 学生端API（成就管理、简历生成等）
  - `admin.py`: 管理员API（用户管理、系统配置等）
  - `common.py`: 公共API（通知、班级列表等）
  - `debate.py`: 辩论赛管理API
  - `ocr.py`: OCR识别API

### 中间件
- **`middleware/`**: 请求处理中间件
  - `cors.py`: CORS跨域配置
  - `logging.py`: 请求日志记录

### 工具
- **`utils.py`**: 通用工具函数

## 数据库架构

详见 `backend/DATABASE_SCHEMA.md`

主要表：
- `users`: 用户表
- `achievements`: 成就荣誉表
- `teacher_relations`: 师生关系表
- `contests`: 辩论赛表
- `contest_participants`: 辩论赛参与者
- `scores`: 评分表
- `audience_votes`: 观众投票表
- `system_settings`: 系统设置表

## 开发规范

### 代码组织
1. **分层架构**: 严格遵循路由层 → 服务层 → 数据层的分层结构
2. **单一职责**: 每个模块只负责一个功能领域
3. **依赖注入**: 使用FastAPI的Depends进行依赖管理

### 测试规范
⚠️ **重要**: 本项目已清理所有测试文件，保持生产代码整洁

**测试开发规范**:
- ✅ 测试代码应放在独立的 `tests/` 目录
- ✅ 使用标准测试框架（如 pytest）
- ✅ 测试文件命名: `test_*.py`
- ❌ 不要在主代码目录混入测试文件
- ❌ 不要将测试结果文件提交到版本控制

**已配置的测试文件忽略规则**:
- `test_*.py`, `*_test.py` - 测试脚本
- `test_*.txt`, `test_*.md` - 测试结果
- `*_output.txt`, `*_result.txt` - 输出文件
- `diagnose*.py`, `diagnose*.log` - 诊断文件
- `run_test*.ps1`, `run_test*.bat` - 测试运行脚本

### Git规范
1. **提交前检查**: 确保不包含测试文件、临时文件、敏感信息
2. **`.gitignore`**: 已配置完善的忽略规则
3. **提交信息**: 清晰描述改动内容

### 环境配置
1. 复制 `.env.example` 为 `.env`
2. 配置必要的环境变量：
   - 数据库连接
   - JWT密钥
   - 阿里云API密钥
   - OpenAI API密钥（可选）

## 快速开始

```powershell
# 1. 进入后端目录
cd backend

# 2. 创建并激活虚拟环境
python -m venv .venv
.\.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入实际配置

# 5. 初始化数据库
python init_db.py

# 6. 启动服务
uvicorn main:app --reload
```

或使用快速启动脚本：
```powershell
.\quickstart.ps1
```

## API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: PostgreSQL (通过SQLAlchemy)
- **认证**: JWT (python-jose)
- **AI服务**: 阿里云百炼 (Qwen-plus)
- **OCR**: 阿里云百炼多模态模型
- **CORS**: 配置支持跨域请求

## 版本历史

- **2026-01-22**: 项目清理，移除测试文件，规范项目结构
- **2026-01-19**: OCR功能测试与验证
- **2026-01-13**: 辩论赛功能开发
- **2025-12-27**: 证书识别功能集成
- **2025-12-18**: 项目初始化

## 维护者

- GitHub: https://github.com/ACDM27/mange_system.git

## 许可证

待定
