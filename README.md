# 🚀 Microblog Platform

A scalable microservice-based blogging platform built with:

* FastAPI
* React / Next.js
* PostgreSQL
* Redis
* RabbitMQ
* Docker
* Celery
* Google OAuth

Designed with modern backend architecture, event-driven communication, and DevOps best practices.

---

# ✨ Features

* JWT Authentication
* Google OAuth Login
* Blog CRUD APIs
* API Gateway
* User Management
* Async Background Tasks
* Redis Caching
* RabbitMQ Messaging
* Dockerized Microservices
* Production-Ready Architecture

---

# 🏗️ Architecture

```text id="g2vh95"
Frontend (Next.js)
        │
        ▼
API Gateway
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Auth   User   Blog
Svc    Svc     Svc
 │       │       │
 └───────┼───────┘
         ▼
     PostgreSQL

         ▼
   Redis / RabbitMQ
```

---

# ⚙️ Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis
* RabbitMQ
* Celery
* Alembic
* Pydantic v2

## Frontend

* React
* Next.js
* TailwindCSS

## DevOps

* Docker
* GitHub Actions
* Nginx
* Prometheus
* Grafana

---

# 📂 Repository Structure

```text id="u8rjhg"
microblog-platform/
│
├── apps/
│   ├── gateway-service/
│   ├── auth-service/
│   ├── user-service/
│   ├── blog-service/
│   └── frontend/
│
│
├── infrastructure/
│   ├── docker/
│   └── monitoring/
│
├── docs/
├── scripts/
├── .github/workflows/
│
├── docker-compose.yml
├── Taskfile.yml
└── README.md
```

---

# 🔧 Services

| Service         | Responsibility                          |
| --------------- | --------------------------------------- |
| Gateway Service | Routing, auth validation, rate limiting |
| Auth Service    | JWT auth, login, register, OAuth        |
| User Service    | Profiles, avatars, preferences          |
| Blog Service    | Posts, tags, categories                 |


# Future Services

| Phase | Service               |
| ----- | --------------------- |
| 1     | Content Moderation    |
| 2     | Semantic Search       |
| 3     | Recommendation Engine |

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/microblog-platform.git

cd microblog-platform
```

## Start Infrastructure

```bash
docker compose up -d
```

## Run Auth Service

```bash id="wq7q2t"
cd apps/auth-service

uv sync

uv run uvicorn app.main:app --reload
```

## Run Frontend

```bash
cd apps/frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://admin:password@localhost:5432/microblog

REDIS_URL=redis://localhost:6379

RABBITMQ_URL=amqp://guest:guest@localhost:5672/

SECRET_KEY=your_secret_key
```

---

# 📘 API Docs

```text id="qarf8n"
http://localhost:8000/docs
```

---

# 🧪 Development Commands

```bash id="r4n2dm"
task up
task down
task test
task lint
task format
```

---

# 🔄 Planned Features

* Notifications Service
* Media Upload Service
* Full-Text Search
* Distributed Tracing
* Kubernetes Deployment
* CI/CD Pipeline
* Multi-Tenant Architecture
* AI-Powered Recommendations

---

# 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Open Pull Request

---

# 📜 License

MIT License

---

# 👨‍💻 Author

Nazmul Alam Diptu
