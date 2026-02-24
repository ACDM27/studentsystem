# Requirements Document

## Introduction

This specification addresses the AI chat functionality in the student portrait system. The current implementation has issues with the POST request format and error handling when communicating with the backend AI chat API. The goal is to ensure reliable communication between the frontend Vue component and the backend Strapi API endpoint for AI-powered student learning assistance.

## Glossary

- **AI Chat Component**: The Vue.js component (`ai-chat.vue`) that provides the user interface for students to interact with the AI learning assistant
- **Chat API**: The backend API endpoint (`/student-portraits/chat`) that processes student questions and returns AI-generated responses
- **Student Portrait**: A data structure containing student learning data, skills, interests, and conversation history
- **Request Payload**: The data structure sent in the POST request to the Chat API
- **Response Format**: The data structure returned by the Chat API containing the AI-generated answer

## Requirements

### Requirement 1

**User Story:** As a student, I want to send questions to the AI assistant, so that I can receive personalized learning guidance based on my student profile.

#### Acceptance Criteria

1. WHEN a student types a question and clicks send THEN the system SHALL transmit the question to the Chat API via POST request
2. WHEN the POST request is constructed THEN the system SHALL include the question text, student ID, and optional context data
3. WHEN the request payload is formatted THEN the system SHALL follow the backend API's expected data structure
4. WHEN the student ID is missing THEN the system SHALL fetch the current user's ID before sending the request
5. WHEN the request is sent THEN the system SHALL display a loading indicator to the student

### Requirement 2

**User Story:** As a developer, I want the API request to use the correct data format, so that the backend can successfully process the request and return a valid response.

#### Acceptance Criteria

1. WHEN the Chat API expects Strapi v5 format THEN the system SHALL wrap the request data in a `data` object
2. WHEN the Chat API expects custom route format THEN the system SHALL send the request data directly without wrapping
3. WHEN the request includes context data THEN the system SHALL serialize it as a JSON string
4. WHEN the backend returns a response THEN the system SHALL extract the AI message from the correct response field
5. WHEN multiple response formats are possible THEN the system SHALL attempt to parse all known formats

### Requirement 3

**User Story:** As a student, I want to see helpful error messages when the AI service is unavailable, so that I understand what went wrong and what to do next.

#### Acceptance Criteria

1. WHEN the Chat API returns a 404 error THEN the system SHALL display a message indicating the endpoint is not configured
2. WHEN the Chat API returns a 500 error THEN the system SHALL display a message indicating a server processing error
3. WHEN a network error occurs THEN the system SHALL display a message indicating connectivity issues
4. WHEN any error occurs THEN the system SHALL log detailed error information to the console for debugging
5. WHEN an error message is displayed THEN the system SHALL provide actionable guidance to the student

### Requirement 4

**User Story:** As a developer, I want comprehensive logging throughout the request lifecycle, so that I can diagnose issues when the AI chat fails.

#### Acceptance Criteria

1. WHEN a chat request is initiated THEN the system SHALL log the question, student ID, and context data
2. WHEN the API call is made THEN the system SHALL log the complete request URL and payload
3. WHEN a response is received THEN the system SHALL log the full response structure and data type
4. WHEN an error occurs THEN the system SHALL log the error status code, message, and response data
5. WHEN response parsing fails THEN the system SHALL log which fields were checked and their values

### Requirement 5

**User Story:** As a student, I want my conversation history to be saved, so that the AI can provide context-aware responses in future interactions.

#### Acceptance Criteria

1. WHEN an AI response is successfully received THEN the system SHALL save the question-answer pair to the student portrait
2. WHEN saving conversation history THEN the system SHALL include the question, answer, timestamp, and category
3. WHEN the student portrait ID is missing THEN the system SHALL skip saving history without blocking the user experience
4. WHEN saving history fails THEN the system SHALL log the error but still display the AI response to the student
5. WHEN the conversation is categorized THEN the system SHALL detect whether it relates to achievement, interest, career, warning, or general topics
