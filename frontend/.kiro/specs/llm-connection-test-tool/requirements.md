# Requirements Document

## Introduction

本规范定义了一个Python脚本工具，用于测试和诊断大语言模型（LLM）API的连接状态。当前项目的AI对话功能存在无法向后端传输用户输入内容的问题，需要一个独立的测试工具来验证后端API的可用性、请求格式的正确性以及响应数据的完整性。该工具将帮助开发者快速定位问题是在前端、后端还是AI服务层面。

## Glossary

- **LLM (Large Language Model)**: 大语言模型，指用于生成AI响应的后端服务
- **Test Script**: 测试脚本，指本规范中要开发的Python诊断工具
- **Backend API**: 后端API，指Strapi服务器提供的 `/api/student-portraits/chat` 接口
- **Connection Test**: 连接测试，指验证网络连通性和API可访问性的测试
- **Request Format Test**: 请求格式测试，指验证API请求数据结构是否符合后端期望的测试
- **Response Validation**: 响应验证，指检查API返回数据的结构和内容是否正确的测试
- **Authentication Test**: 认证测试，指验证JWT token是否有效以及权限是否正确的测试

## Requirements

### Requirement 1

**User Story:** 作为开发者，我想要测试后端API的基本连通性，以便确认服务器是否正常运行且可访问。

#### Acceptance Criteria

1. WHEN the Test Script is executed THEN the system SHALL attempt to connect to the configured backend URL
2. WHEN the connection test runs THEN the system SHALL report whether the backend server is reachable
3. WHEN the backend is unreachable THEN the system SHALL display the connection error details including timeout and network issues
4. WHEN the backend is reachable THEN the system SHALL display the server response time
5. WHEN testing multiple endpoints THEN the system SHALL test both the health check endpoint and the chat API endpoint

### Requirement 2

**User Story:** 作为开发者，我想要验证不同的请求数据格式，以便找出后端API期望的正确格式。

#### Acceptance Criteria

1. WHEN the Test Script sends a request THEN the system SHALL test both wrapped format (Strapi v5 style with `data` wrapper) and direct format
2. WHEN testing request formats THEN the system SHALL include all required fields: question, student_id, and optional context
3. WHEN a request format succeeds THEN the system SHALL display which format was accepted by the backend
4. WHEN a request format fails THEN the system SHALL display the HTTP status code and error message
5. WHEN testing is complete THEN the system SHALL provide a recommendation on which format to use in the frontend

### Requirement 3

**User Story:** 作为开发者，我想要验证JWT认证是否正常工作，以便确认权限问题不是导致API失败的原因。

#### Acceptance Criteria

1. WHEN the Test Script requires authentication THEN the system SHALL accept a JWT token as input parameter
2. WHEN a token is provided THEN the system SHALL include it in the Authorization header as "Bearer {token}"
3. WHEN testing without a token THEN the system SHALL report whether the endpoint requires authentication
4. WHEN a token is invalid THEN the system SHALL display the authentication error message
5. WHEN a token is valid THEN the system SHALL confirm successful authentication

### Requirement 4

**User Story:** 作为开发者，我想要查看完整的请求和响应数据，以便理解数据流和调试问题。

#### Acceptance Criteria

1. WHEN the Test Script sends a request THEN the system SHALL log the complete request URL, headers, and body
2. WHEN a response is received THEN the system SHALL log the complete response status, headers, and body
3. WHEN displaying data THEN the system SHALL format JSON data with proper indentation for readability
4. WHEN an error occurs THEN the system SHALL display both the error message and the full error response
5. WHEN verbose mode is enabled THEN the system SHALL display additional debugging information including timestamps

### Requirement 5

**User Story:** 作为开发者，我想要验证响应数据的结构，以便确认前端能否正确解析AI的回复。

#### Acceptance Criteria

1. WHEN a successful response is received THEN the system SHALL check for the presence of AI response fields (response, message, answer, reply)
2. WHEN the response structure is analyzed THEN the system SHALL display which fields are present and their data types
3. WHEN the AI response text is found THEN the system SHALL display a preview of the content
4. WHEN the response structure is unexpected THEN the system SHALL suggest possible field names to check in the frontend
5. WHEN multiple response formats are detected THEN the system SHALL document all possible formats for frontend compatibility

### Requirement 6

**User Story:** 作为开发者，我想要运行一系列自动化测试，以便快速诊断AI聊天功能的所有潜在问题。

#### Acceptance Criteria

1. WHEN the Test Script runs in full test mode THEN the system SHALL execute all test cases sequentially
2. WHEN all tests complete THEN the system SHALL display a summary report with pass/fail status for each test
3. WHEN any test fails THEN the system SHALL provide specific recommendations for fixing the issue
4. WHEN all tests pass THEN the system SHALL confirm that the backend API is fully functional
5. WHEN generating the report THEN the system SHALL include timestamps, test duration, and detailed results

### Requirement 7

**User Story:** 作为开发者，我想要配置测试参数，以便在不同环境（开发、测试、生产）中使用该工具。

#### Acceptance Criteria

1. WHEN the Test Script is executed THEN the system SHALL accept command-line arguments for backend URL, token, and student ID
2. WHEN no arguments are provided THEN the system SHALL use default values from a configuration file or environment variables
3. WHEN a configuration file is used THEN the system SHALL support JSON or YAML format
4. WHEN environment variables are set THEN the system SHALL prioritize them over configuration file values
5. WHEN displaying configuration THEN the system SHALL mask sensitive data like tokens in the output

### Requirement 8

**User Story:** 作为开发者，我想要测试不同的学生ID和问题内容，以便验证API在各种输入下的行为。

#### Acceptance Criteria

1. WHEN the Test Script accepts test data THEN the system SHALL allow custom question text and student ID as parameters
2. WHEN no test data is provided THEN the system SHALL use predefined sample questions
3. WHEN testing with context data THEN the system SHALL allow optional student portrait context to be included
4. WHEN multiple test cases are defined THEN the system SHALL execute them sequentially and report results for each
5. WHEN a test case fails THEN the system SHALL continue with remaining test cases and report all results at the end
