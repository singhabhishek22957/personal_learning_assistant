# Personal Learning Assistant (AI-Powered)

An AI-powered personal learning platform designed to help users learn new technologies, conduct research, manage study plans, organize knowledge, and improve productivity through personalized AI assistance.

> **Project Status:** 🚧 Initial Development

## Overview

Personal Learning Assistant is a centralized platform that combines AI-powered learning, research, document management, and productivity tools.

The goal is to provide users with a personalized learning environment where they can explore new subjects, understand complex concepts, organize learning materials, generate documents, and track their learning progress.

## Core Features

### 1. AI Learning Assistant
- Learn new technologies and subjects.
- Generate structured learning roadmaps.
- Break complex topics into manageable lessons.
- Explain concepts with practical examples.
- Identify knowledge gaps and suggest improvements.

### 2. AI Research Assistant
- Research topics using AI.
- Search and analyze relevant information.
- Summarize research materials.
- Organize research sources.
- Generate research notes and reports.

### 3. Document & Knowledge Management
- Upload and manage learning documents.
- Read and analyze PDF documents.
- Ask questions about uploaded documents using RAG.
- Generate notes, summaries, assignments, and reports.
- Save AI-generated documents in Markdown format.
- Edit and manage document versions.

### 4. Smart Study Planner
- Create daily, weekly, and monthly study plans.
- Organize learning tasks and deadlines.
- Track task completion.
- Monitor learning progress.
- Plan future learning activities.

### 5. Assessment & Progress Tracking
- Generate quizzes and assignments.
- Evaluate submitted answers.
- Identify weak topics.
- Track learning performance.
- Recommend revision activities.

### 6. Resource Discovery
- Discover useful learning resources.
- Find documentation, books, and tutorials.
- Organize learning resources by topic.

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | Next.js, React, TypeScript |
| UI | Tailwind CSS, Shadcn UI |
| Backend | Python, FastAPI |
| AI Integration | LangChain, LangGraph |
| LLM | Gemini / OpenAI / Ollama |
| Database | MongoDB |
| Vector Database | Qdrant |
| Cache & Queue | Redis |
| Background Jobs | Celery |
| Authentication | JWT |
| Containerization | Docker, Docker Compose |
| Document Processing | PyMuPDF, Markdown |

*The technology stack and integrations may evolve during development.*

## High-Level Architecture

```text
                 CLIENT
                   |
                   v
             NEXT.JS FRONTEND
                   |
                   v
              FASTAPI BACKEND
                   |
          +--------+---------+
          |        |         |
          v        v         v
       AUTH     SERVICES   AI LAYER
                           |
                           v
                       LANGGRAPH
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          LEARNING      RESEARCH       PLANNER
             |             |             |
             +-------------+-------------+
                           |
                           v
                       LANGCHAIN
                           |
                 +---------+---------+
                 |                   |
                 v                   v
              LLMs              RAG SYSTEM
                                     |
                                     v
                                  QDRANT

       MONGODB       REDIS       CELERY WORKERS
```

## Project Structure

```text
personal_learning_assistant/
│
├── server/
│   ├── app/
│   │   ├── core/
│   │   ├── dependencies/
│   │   ├── middleware/
│   │   ├── modules/
│   │   ├── shared/
│   │   └── main.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── client/
│   └── (Frontend application - planned)
│
├── docker-compose.yml
│
├── .gitignore
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker Desktop
- Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>

cd personal_learning_assistant
```

### 2. Configure Environment Variables

Create your backend environment file:

```bash
cp server/.env.example server/.env
```

Configure the required environment variables.

Example:

```env
APP_NAME=Personal Learning Assistant
ENVIRONMENT=development

MONGO_URI=mongodb://admin:password@mongo:27017/personal_learning_assistant?authSource=admin
REDIS_URL=redis://redis:6379/0

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use strong secrets in real deployments. Never commit `.env` files.

### 3. Start Services Using Docker

```bash
docker compose up -d --build
```

### 4. View Application Logs

```bash
docker compose logs -f server
```

### 5. Access API Documentation

```text
http://localhost:8000/docs
```

## Development Roadmap

- [x] Initial backend project setup
- [x] Docker Compose configuration
- [x] MongoDB and Redis integration
- [x] Logging middleware
- [x] FastAPI lifespan setup
- [x] Authentication dependencies
- [ ] User registration and login
- [ ] User profile management
- [ ] Learning module
- [ ] Research module
- [ ] Document management
- [ ] RAG pipeline
- [ ] AI agent orchestration with LangGraph
- [ ] Study planner
- [ ] Assessment and progress tracking
- [ ] Frontend integration
- [ ] Google Calendar integration

## Project Goals

The long-term goal is to build a personal AI learning environment that combines:

- Personalized learning
- AI-powered research
- Knowledge management
- Intelligent planning
- Document generation
- Continuous learning assessment

## Contribution

This project is currently under active development. Contributions, suggestions, and feedback are welcome.

## License

To be decided.