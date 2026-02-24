# Design Document

## Overview

本设计文档描述了一个Python命令行工具，用于诊断和测试大语言模型API的连接问题。该工具将执行一系列测试来验证后端API的可用性、请求格式、认证机制和响应结构，并提供详细的错误报告和修复建议。

## Architecture

### 系统架构

```
┌─────────────────┐
│  Test Script    │
│  (Python CLI)   │
└────────┬────────┘
         │
         ├─ Configuration Module
         │  └─ 读取配置文件/环境变量/命令行参数
         │
         ├─ Connection Test Module  
         │  └─ 测试网络连通性和服务器可达性
         │
         ├─ Authentication Test Module
         │  └─ 验证JWT token有效性
         │
         ├─ Request Format Test Module
         │  └─ 测试不同的请求数据格式
         │
         ├─ Response Validation Module
         │  └─ 验证响应数据结构
         │
         └─ Report Generator Module
            └─ 生成测试报告和修复建议
```

### 技术栈

- **Python 3.8+**: 主要编程语言
- **requests**: HTTP请求库
- **argparse**: 命令行参数解析
- **json**: JSON数据处理
- **colorama**: 终端彩色输出
- **tabulate**: 表格格式化输出

## Components and Interfaces

### 1. Configuration Module

**职责**: 管理测试配置参数

**接口**:
```python
class Config:
    def __init__(self):
        self.backend_url: str
        self.token: Optional[str]
        self.student_id: str
        self.verbose: bool
        
    @classmethod
    def from_args(cls, args) -> Config
    
    @classmethod
    def from_env(cls) -> Config
    
    def validate(self) -> bool
```

### 2. Connection Test Module

**职责**: 测试后端服务器连通性

**接口**:
```python
class ConnectionTester:
    def __init__(self, config: Config):
        self.config = config
        
    def test_server_reachable(self) -> TestResult
    
    def test_endpoint_exists(self, endpoint: str) -> TestResult
    
    def measure_response_time(self) -> float
```

### 3. Authentication Test Module

**职责**: 验证JWT认证

**接口**:
```python
class AuthTester:
    def __init__(self, config: Config):
        self.config = config
        
    def test_with_token(self) -> TestResult
    
    def test_without_token(self) -> TestResult
    
    def validate_token_format(self) -> bool
```

### 4. Request Format Test Module

**职责**: 测试不同的请求格式

**接口**:
```python
class RequestFormatTester:
    def __init__(self, config: Config):
        self.config = config
        
    def test_wrapped_format(self, question: str) -> TestResult
    
    def test_direct_format(self, question: str) -> TestResult
    
    def test_with_context(self, question: str, context: dict) -> TestResult
```

### 5. Response Validation Module

**职责**: 验证响应数据结构

**接口**:
```python
class ResponseValidator:
    def __init__(self):
        self.known_response_fields = ['response', 'message', 'answer', 'reply']
        
    def validate_structure(self, response: dict) -> ValidationResult
    
    def extract_ai_message(self, response: dict) -> Optional[str]
    
    def analyze_fields(self, response: dict) -> dict
```

### 6. Report Generator Module

**职责**: 生成测试报告

**接口**:
```python
class ReportGenerator:
    def __init__(self):
        self.results: List[TestResult] = []
        
    def add_result(self, result: TestResult)
    
    def generate_summary(self) -> str
    
    def generate_recommendations(self) -> List[str]
    
    def print_report(self)
```

## Data Models

### TestResult

```python
@dataclass
class TestResult:
    test_name: str
    status: str  # 'PASS', 'FAIL', 'WARN'
    message: str
    details: Optional[dict] = None
    duration: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
```

### ValidationResult

```python
@dataclass
class ValidationResult:
    is_valid: bool
    found_fields: List[str]
    missing_fields: List[str]
    ai_message: Optional[str]
    suggestions: List[str]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Connection test reliability
*For any* valid backend URL, when the connection test is executed, the test result should accurately reflect whether the server is reachable or not
**Validates: Requirements 1.1, 1.2**

### Property 2: Request format detection
*For any* API endpoint, when testing multiple request formats, at least one format should be identified as accepted if the endpoint is functional
**Validates: Requirements 2.1, 2.3**

### Property 3: Authentication validation
*For any* JWT token provided, the authentication test should correctly determine whether the token is valid and accepted by the backend
**Validates: Requirements 3.2, 3.4**

### Property 4: Response field extraction
*For any* successful API response containing an AI message, the response validator should be able to extract the message from at least one of the known response fields
**Validates: Requirements 5.1, 5.3**

### Property 5: Test execution completeness
*For any* test suite execution, when one test fails, all remaining tests should still execute and report their results
**Validates: Requirements 8.5**

### Property 6: Configuration precedence
*For any* configuration parameter, when multiple sources provide values (CLI args, env vars, config file), the system should apply the correct precedence order
**Validates: Requirements 7.2, 7.4**

## Error Handling

### 网络错误处理

- **连接超时**: 设置30秒超时，超时后报告连接失败
- **DNS解析失败**: 检测并报告域名无法解析
- **连接拒绝**: 检测并报告服务器拒绝连接
- **SSL错误**: 检测并报告证书验证问题

### API错误处理

- **404错误**: 报告端点不存在，建议检查后端路由配置
- **500错误**: 报告服务器内部错误，显示错误详情
- **401/403错误**: 报告认证/授权失败，建议检查token
- **400错误**: 报告请求格式错误，显示后端期望的格式

### 数据验证错误

- **响应格式不匹配**: 列出所有检查的字段，建议可能的字段名
- **JSON解析失败**: 显示原始响应内容
- **缺少必需字段**: 列出缺少的字段和建议

## Testing Strategy

### Unit Testing

使用Python的`unittest`框架进行单元测试：

- **Configuration Module Tests**: 测试配置加载和验证逻辑
- **Response Validator Tests**: 测试响应字段提取逻辑
- **Report Generator Tests**: 测试报告生成格式

### Property-Based Testing

使用`hypothesis`库进行属性测试：

- **Property 1 Test**: 生成随机URL，验证连接测试的准确性
- **Property 2 Test**: 生成随机请求数据，验证格式检测逻辑
- **Property 4 Test**: 生成随机响应结构，验证字段提取逻辑

### Integration Testing

- 使用mock服务器测试完整的测试流程
- 测试不同的错误场景和响应格式
- 验证报告生成的完整性

### Manual Testing

- 在实际后端环境中运行测试脚本
- 验证错误消息的清晰度和有用性
- 确认修复建议的准确性

## Implementation Notes

### 命令行接口设计

```bash
# 基本用法
python test_llm_connection.py --url http://localhost:1337 --student-id 123

# 带认证
python test_llm_connection.py --url http://localhost:1337 --token "eyJ..." --student-id 123

# 详细模式
python test_llm_connection.py --url http://localhost:1337 --student-id 123 --verbose

# 自定义问题
python test_llm_connection.py --url http://localhost:1337 --student-id 123 --question "测试问题"

# 使用配置文件
python test_llm_connection.py --config config.json
```

### 输出格式示例

```
╔══════════════════════════════════════════════════════════════╗
║          LLM Connection Test Tool v1.0                       ║
╚══════════════════════════════════════════════════════════════╝

[1/6] Testing server connectivity...
  ✓ Server is reachable (Response time: 45ms)

[2/6] Testing endpoint existence...
  ✓ Endpoint /api/student-portraits/chat exists

[3/6] Testing authentication...
  ✓ JWT token is valid
  ✓ Authentication successful

[4/6] Testing request format (wrapped)...
  ✗ Format rejected (Status: 400)
  Error: Invalid request structure

[5/6] Testing request format (direct)...
  ✓ Format accepted (Status: 200)
  Response time: 1.2s

[6/6] Validating response structure...
  ✓ Response contains 'response' field
  ✓ AI message extracted successfully
  Preview: "根据您的学习画像分析..."

╔══════════════════════════════════════════════════════════════╗
║                    Test Summary                              ║
╚══════════════════════════════════════════════════════════════╝

Total Tests: 6
Passed: 5
Failed: 1
Warnings: 0

╔══════════════════════════════════════════════════════════════╗
║                  Recommendations                             ║
╚══════════════════════════════════════════════════════════════╝

✓ Backend API is functional
✓ Use DIRECT format (not wrapped) for requests
✓ Response field to use: 'response'

Frontend Code Suggestion:
  const aiMessage = response.response || response.message

All tests completed in 2.5 seconds.
```

### 配置文件格式

```json
{
  "backend_url": "http://localhost:1337",
  "api_prefix": "/api",
  "chat_endpoint": "/student-portraits/chat",
  "timeout": 30,
  "test_questions": [
    "请分析我的学习成果数据",
    "根据我的兴趣推荐相关课程"
  ],
  "default_student_id": "123"
}
```
