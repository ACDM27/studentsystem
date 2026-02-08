# Backend API Reference & Frontend Integration Guide

This document provides a comprehensive reference for the backend API and guidelines for frontend integration. It is designed to help frontend developers understand the data structures, request flows, and best practices for connecting with the backend.

## 1. General Information

- **Base URL**: `http://localhost:8000` (Local development)
- **API Prefix**: `/api` (varies by module, see below)
- **Time Format**: ISO 8601 (e.g., `2023-10-27T10:00:00`)

### Standard Response Format
All API responses follow a consistent wrapper structure. Frontend interceptors should handle this unwrapping globally.

```typescript
interface ApiResponse<T = any> {
  code: number;      // 200 for success, non-200 for logical errors
  msg: string;       // User-facing message
  data: T;           // The actual payload
}
```

### Authentication
- **Method**: Bearer Token
- **Header**: `Authorization: Bearer <your_jwt_token>`
- **Token Source**: Returned in `login` response.
- **Expiration**: Handle 401 responses by redirecting to login.

---

## 2. API Modules & Endpoints

### 2.1 Authentication (`/api/v1/auth`)

#### Login
- **Endpoint**: `POST /api/v1/auth/login`
- **Request**:
  ```json
  {
    "username": "student_username",
    "password": "password123"
  }
  ```
- **Response Data**:
  ```json
  {
    "token": "eyJhbG...",
    "userInfo": {
      "id": 1,
      "name": "Student Name",
      "role": "student" // or "admin"
    }
  }
  ```

---

### 2.2 Common Resources (`/api/v1/common`)

#### Get Teacher List
Used for populating dropdowns in forms.
- **Endpoint**: `GET /api/v1/common/teachers`
- **Auth**: Required
- **Response Data**: Array of teachers
  ```json
  [
    {
      "id": 1,
      "name": "Teacher Name",
      "department": "Computer Science"
    }
  ]
  ```

#### Upload File
Generic file upload (note: specialized certificate upload exists in Student module).
- **Endpoint**: `POST /api/v1/common/upload`
- **Content-Type**: `multipart/form-data`
- **Form Field**: `file`
- **Response Data**: `{"url": "/uploads/filename.ext"}`

---

### 2.3 Student Module (`/api/v1/student`)
*Role Required: student*

#### 1. Certificate Recognition (OCR) - Step 1
Uploads a certificate and uses AI to extract information.
- **Endpoint**: `POST /api/v1/student/ocr/recognize`
- **Content-Type**: `multipart/form-data`
- **Form Field**: `file`
- **Response Data**:
  ```json
  {
    "recognized_data": {
      "title": "Award Name",
      "date": "2023-01-01",
      "issuer": "Organization",
      "recipient_name": "Student Name",
      "suggested_type": "Competition"
      // ... detailed extracted fields
    },
    "file_url": "/uploads/students/1/certs/uuid.jpg", // KEEP THIS for Step 2
    "file_info": { ... }
  }
  ```

#### 2. Submit Achievement - Step 2
Submits the confirmed/consulted data creating a database record.
- **Endpoint**: `POST /api/v1/student/achievements`
- **Request**:
  ```json
  {
    "title": "Award Name",
    "teacher_id": 1,          // Selected from Teacher List
    "type": "Competition",
    "content_json": { ... },  // The full recognized_data object
    "evidence_url": "..."     // The file_url from Step 1
  }
  ```

#### Get My Achievements
- **Endpoint**: `GET /api/v1/student/achievements`
- **Query Params**: `?status=pending` (optional)
- **Response Data**: Array of achievements

#### Get Student Persona
Fetches the AI-generated analysis of the student.
- **Endpoint**: `GET /api/v1/student/persona`
- **Response Data**:
  ```json
  {
    "strengths": ["Math", "Logic"],
    "achievements_summary": "...",
    "suggested_improvements": ["..."]
  }
  ```

#### AI Chat
Chat with an AI assistant that has context of the student's achievements (RAG).
- **Endpoint**: `POST /api/v1/student/ai/chat`
- **Request**:
  ```json
  {
    "session_id": "optional-uuid", // Omit for new session, provide to continue
    "message": "User query"
  }
  ```
- **Response Data**:
  ```json
  {
    "session_id": "uuid",
    "message": "AI response"
  }
  ```

---

### 2.4 Admin Module (`/api/v1/admin`)
*Role Required: admin*

#### Get Achievements for Review
- **Endpoint**: `GET /api/v1/admin/achievements`
- **Query Params**:
  - `page`: int (default 1)
  - `page_size`: int (default 10)
  - `status`: string (pending/approved/rejected)
  - `student_name`: string (search)
- **Response Data**:
  ```json
  {
    "list": [ ... ],
    "total": 50
  }
  ```

#### Audit Achievement
Approve or reject a submission.
- **Endpoint**: `PATCH /api/v1/admin/achievements/{id}/audit`
- **Request**:
  ```json
  {
    "action": "approve", // or "reject"
    "comment": "Optional comment" // Required if rejected
  }
  ```

---

### 2.5 Certificate Utility (`/api/certificate`)
General certificate utilities.

#### Batch Recognize
- **Endpoint**: `POST /api/certificate/batch-recognize`
- **Content-Type**: `multipart/form-data`
- **Form Field**: `files` (array of files)

---

## 3. Frontend Optimization & Integration Strategy

### 3.1 HTTP Client Setup (Axios)
Create a central `request.ts` or `http.ts` file to handle the boilerplate.

1.  **Base Config**: Set `baseURL` from environment variable (`VITE_API_URL` or similar).
2.  **Request Interceptor**:
    -   Read token from `localStorage` (e.g., key `token`).
    -   If exists, add header: `config.headers.Authorization = 'Bearer ' + token`.
3.  **Response Interceptor**:
    -   Check `response.data.code`.
    -   If `code === 200`: Return `response.data.data` (unwrap automatically).
    -   If `code === 401`: Clear token, redirect to `/login`.
    -   Else: Throw error with `response.data.msg` to be caught by UI components.

### 3.2 Type Definitions
Create a `types` folder (e.g., `src/types/api`) to mirror backend usage.

```typescript
// src/types/api/models.ts
export interface UserInfo {
  id: number;
  name: string;
  role: 'student' | 'admin';
}

export interface Achievement {
  id: number;
  title: string;
  type: string;
  status: 'pending' | 'approved' | 'rejected';
  create_time: string;
  // ...
}
```

### 3.3 The "Certificate Submission" Flow
This is a complex 2-step process. Frontend logic should be:

1.  **Step 1 (Upload)**:
    -   User selects file -> Calls `/api/v1/student/ocr/recognize`.
    -   Show "Processing..." loading state (can take seconds as it calls AI).
    -   **On Success**: Store `file_url`, `file_info`, and `recognized_data` in local state.
    -   **Display Form**: Pre-fill a form with `recognized_data`.

2.  **Step 2 (Verification & Submit)**:
    -   User reviews the pre-filled form (corrects typos, etc.).
    -   User selects a **Teacher** (fetch list from `/api/v1/common/teachers` on mount).
    -   On "Submit" click -> Calls `/api/v1/student/achievements`.
    -   Payload must include `evidence_url` (from Step 1 response) and the final form data.

### 3.4 Data Caching
-   **Static Data**: The Teacher list (`/api/v1/common/teachers`) changes rarely. Fetch once on app load or store in a global store (Pinia/Vuex) to avoid checking on every form load.
-   **User Info**: Store in global state after Login.

### 3.5 Error Handling
-   Backend validates file types and sizes. Handle 400 errors gracefully by showing toast notifications.
-   OCR can fail or return low confidence. Allow users to manually edit *all* fields if the AI guesses wrong.
