# User Service

## Overview

The User Service is responsible for managing users in the microblog platform.

This microservice handles:

* User registration
* Authentication integration
* User profile management
* Follow/unfollow relationships
* Account settings
* User search
* User activity metadata

---

# Responsibilities

## Core Responsibilities

* Manage user accounts
* Store user profile information
* Handle user relationships
* Expose user-related APIs
* Maintain user preferences/settings

---

# Planned Features

## Phase 1 — Foundation

* [x] FastAPI setup
* [x] Health check endpoint
* [x] Environment configuration
* [ ] Logging setup
* [ ] Docker support
* [x] Ruff + MyPy + Pytest
* [x] Structured project architecture

---

## Phase 2 — Database Layer

* [ ] PostgreSQL integration
* [ ] SQLAlchemy setup
* [ ] Alembic migrations
* [ ] Database session management
* [ ] Base model implementation

---

## Phase 3 — User Model

* [ ] UUID-based user model
* [ ] Username support
* [ ] Email support
* [ ] Password hashing
* [ ] User roles
* [ ] Profile image support
* [ ] Bio support
* [ ] Verification status

---

## Phase 4 — Authentication

* [ ] JWT authentication
* [ ] Access tokens
* [ ] Refresh tokens
* [ ] Login endpoint
* [ ] Logout endpoint
* [ ] Password reset
* [ ] Email verification

---

## Phase 5 — User Profile APIs

* [ ] Create user
* [ ] Get user
* [ ] Update profile
* [ ] Delete account
* [ ] Upload avatar
* [ ] Update password

---

## Phase 6 — Social Features

* [ ] Follow users
* [ ] Unfollow users
* [ ] Followers list
* [ ] Following list
* [ ] Mutual follows
* [ ] User recommendations

---

## Phase 7 — Search Features

* [ ] Search users
* [ ] Username autocomplete
* [ ] Trending creators
* [ ] User ranking

---

## Phase 8 — Background Tasks

* [ ] Welcome email
* [ ] Notification events
* [ ] Analytics events
* [ ] Avatar processing

---

## Phase 9 — Observability

* [ ] Structured logging
* [ ] Prometheus metrics
* [ ] Grafana dashboards
* [ ] OpenTelemetry tracing
* [ ] Error monitoring

---

# API Endpoints (Planned)

## Health

| Method | Endpoint  | Description  |
| ------ | --------- | ------------ |
| GET    | `/health` | Health check |

---

## Authentication

| Method | Endpoint                | Description   |
| ------ | ----------------------- | ------------- |
| POST   | `/api/v1/auth/register` | Register user |
| POST   | `/api/v1/auth/login`    | Login         |
| POST   | `/api/v1/auth/refresh`  | Refresh token |
| POST   | `/api/v1/auth/logout`   | Logout        |

---

## Users

| Method | Endpoint             | Description    |
| ------ | -------------------- | -------------- |
| GET    | `/api/v1/users/me`   | Current user   |
| GET    | `/api/v1/users/{id}` | Get user       |
| PATCH  | `/api/v1/users/me`   | Update profile |
| DELETE | `/api/v1/users/me`   | Delete account |

---

## Social

| Method | Endpoint                       | Description   |
| ------ | ------------------------------ | ------------- |
| POST   | `/api/v1/users/{id}/follow`    | Follow user   |
| DELETE | `/api/v1/users/{id}/follow`    | Unfollow user |
| GET    | `/api/v1/users/{id}/followers` | Followers     |
| GET    | `/api/v1/users/{id}/following` | Following     |

---

# Tech Stack

| Layer            | Technology |
| ---------------- | ---------- |
| API              | FastAPI    |
| Database         | PostgreSQL |
| ORM              | SQLAlchemy |
| Migrations       | Alembic    |
| Validation       | Pydantic   |
| Background Jobs  | Celery     |
| Queue            | Redis      |
| Testing          | Pytest     |
| Linting          | Ruff       |
| Type Checking    | MyPy       |
| Containerization | Docker     |

---

# Local Development

## Run Service

```bash
task run-service -- user-service 8001
```

---

## Install Dependencies

```bash
uv add fastapi uvicorn
```

---

## Run Tests

```bash
task test
```

---

## Run Linting

```bash
task lint
```

---

## Format Code

```bash
task format
```

---

# Future Improvements

* OAuth2 login
* Google authentication
* GitHub authentication
* User verification badges
* Recommendation embeddings
* Activity feeds
* GraphQL support
* Event-driven architecture
* CQRS pattern
* Kafka integration

---

# Service Port

| Service      | Port |
| ------------ | ---- |
| user-service | 8001 |

---

# Status

Current Phase: Foundation Setup
