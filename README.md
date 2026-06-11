# Project Management Dashboard API

## Overview

This project is a backend service for managing project profiles and related documents.
The application allows users to create, update, share, and delete project information, including project details and attached files.

The system supports authentication, project-level permissions, document storage, and optional cloud-based file processing using AWS services.

---

## Tech Stack

* Python 3.12+
* FastAPI
* PostgreSQL
* SQLAlchemy or another ORM
* Docker
* AWS S3 for file storage
* AWS Lambda for optional file/image processing
* GitHub Actions or GitLab CI for CI/CD

---

## Main Features

### Authentication

* User registration
* User login
* JWT-based authorization
* JWT token validity: 1 hour

### Project Management

* Create projects
* View projects accessible to the authenticated user
* Update project details
* Delete projects
* Assign project owner automatically during project creation

### Document Management

* Upload project documents
* Supported document types: `docx`, `pdf`
* Update documents
* Delete documents
* Download documents if the user has access to the related project
* Store documents in AWS S3

### Access Control

The application supports two types of project access:

#### Owner

The project creator becomes the owner automatically.
The owner can:

* View project details
* Update project details
* Upload documents
* Update documents
* Delete documents
* Delete the project
* Invite other users to the project

#### Participant

A participant is a user invited by the project owner.
A participant can:

* View project details
* Update project details
* Upload documents
* Update documents
* Delete documents

A participant cannot:

* Delete the project
* Invite other users

---

## API Endpoints

### Authentication

#### Register User

```http
POST /auth
```

Creates a new user account.

Request body:

```json
{
  "login": "user_login",
  "password": "password",
  "repeat_password": "password"
}
```

---

#### Login

```http
POST /login
```

Authenticates the user and returns a JWT access token.

Request body:

```json
{
  "login": "user_login",
  "password": "password"
}
```

Response example:

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

---

## Project Endpoints

### Create Project

```http
POST /projects
```

Creates a new project from provided details.
The authenticated user automatically becomes the project owner.

Request body:

```json
{
  "name": "Project name",
  "description": "Project description"
}
```

---

### Get Accessible Projects

```http
GET /projects
```

Returns all projects accessible to the authenticated user.

The response should include:

* Project details
* Project documents
* User access role

---

### Get Project Details

```http
GET /projects/{project_id}/info
```

Returns project details if the authenticated user has access to the project.

---

### Update Project Details

```http
PUT /projects/{project_id}/info
```

Updates project details.

Request body:

```json
{
  "name": "Updated project name",
  "description": "Updated project description"
}
```

Returns the updated project information.

---

### Delete Project

```http
DELETE /projects/{project_id}
```

Deletes the project and all related documents.

Only the project owner can perform this operation.

---

## Document Endpoints

### Get Project Documents

```http
GET /projects/{project_id}/documents
```

Returns all documents assigned to a specific project.

---

### Upload Project Documents

```http
POST /projects/{project_id}/documents
```

Uploads one or more documents for a specific project.

Supported file types:

* `.pdf`
* `.docx`

---

### Download Document

```http
GET /documents/{document_id}
```

Downloads a document if the authenticated user has access to the related project.

---

### Update Document

```http
PUT /documents/{document_id}
```

Updates an existing document.

---

### Delete Document

```http
DELETE /documents/{document_id}
```

Deletes a document and removes it from the related project.

---

## Sharing and Invitations

### Invite User to Project

```http
POST /projects/{project_id}/invite?user={login}
```

Grants access to a specific user.

Rules:

* Only the project owner can invite users.
* Invited users receive participant permissions.
* If the request is not made by the project owner, the API should return an error.

---

## Optional Sharing Feature

### Share Project by Email

```http
GET /projects/{project_id}/share?with={email}
```

Sends a project join link to the provided email address.

The link should contain a secure hashed token that allows another user to join the project through a browser.

---

## Phase 2 Additional Tasks

### Database

* Design normalized database tables
* Add denormalized structures where useful for performance
* Create the database with ORM
* Optionally create the database without ORM for comparison

### AWS S3 and Lambda

* Store uploaded files in AWS S3
* Trigger AWS Lambda on S3 events
* Optional: resize uploaded images
* Calculate the total size of project files
* Apply a file size limit per project

### Testing

* Add unit tests
* Add integration tests
* Test authentication and authorization logic
* Test project and document access permissions

### CI/CD

Configure GitHub Actions or GitLab CI for:

* Running tests
* Running linters
* Building Docker images
* Pushing images to a container registry
* Deploying to cloud after merge

### Packaging and Tooling

Add project tooling such as:

* `pyproject.toml`
* `tox` or `poetry`
* Code formatting
* Linting
* Type checking

### Validation

All request and response data should be validated with Pydantic models.

---

## Implementation Notes

* All API responses should be returned in JSON format, except file downloads.
* The API should return proper HTTP status codes.
* All business logic endpoints must be protected with JWT authorization.
* User access permissions should be resolved from the JWT-authenticated user.
* Project owners have full access to their projects.
* Project participants can modify project data and documents but cannot delete the project.
* Exact endpoint names and parameters may be adjusted after agreement with the mentor, as long as the required business logic is covered.

---

## Suggested HTTP Status Codes

| Situation                |                 Status Code |
| ------------------------ | --------------------------: |
| Successful request       |                    `200 OK` |
| Resource created         |               `201 Created` |
| Successful deletion      |            `204 No Content` |
| Invalid request data     |           `400 Bad Request` |
| Missing or invalid token |          `401 Unauthorized` |
| User has no permission   |             `403 Forbidden` |
| Resource not found       |             `404 Not Found` |
| Validation error         |  `422 Unprocessable Entity` |
| Server error             | `500 Internal Server Error` |
