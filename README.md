# To-Do List RPG

A gamified task management API built with FastAPI, PostgreSQL, Redis, and Docker.

Users can create and organize tasks while progressing through an RPG-inspired system. Completing tasks grants experience and gold, allowing users to level up, improve skills, purchase items from the shop, and track their overall progress.

## Quick start

### Requirements

- Docker
- Docker Compose

### Getting Started

1. Rename the `.env.example` file to `.env`.

2. Configure the required environment variables in `.env`.

3. Build and start the application:

```bash
docker compose up --build
```

The first launch may take a few minutes because Docker will download the required images and build the application.

### API Documentation

After the application starts, the Swagger UI will be available at:

http://127.0.0.1:8000/docs#/

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- Taskiq
- Docker & Docker Compose

## Features

### Authentication & User Management

- Session-based authentication
- User registration and login
- Profile management
- Account deletion

### Task Management

- Create, update, and delete tasks
- Categories, priorities, difficulties, and deadlines
- Recurring tasks
- Soft deletion
- Task filtering and sorting
- Task completion and rollback
- Automatic reward calculation
- Task history

### RPG System

- Experience and leveling
- Gold rewards
- Skill progression
- Rank progression

### Skills

- Skill management
- Experience gained from completed tasks
- Skill level progression

### Categories

- Category management
- Task organization

### Shop & Inventory

- Shop management
- Item purchasing
- Skill-based item requirements
- Inventory management
- Item usage

### Economy

- Transaction history
- Purchase logging
- Balance tracking

### Statistics

- User progress overview
- Task statistics
- Skill statistics



