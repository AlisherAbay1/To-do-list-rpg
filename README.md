````md
# To-Do List RPG

A gamified task management application built with FastAPI, PostgreSQL, Redis, and Docker.

## Requirements

- Docker
- Docker Compose

## Getting Started

1. Rename the `.env.example` file to `.env`.

2. Configure the required environment variables in `.env`.

3. Build and start the application:

```bash
docker compose up --build
```

The first launch may take a few minutes because Docker will download the required images and build the application.

## API Documentation

After the application starts, the Swagger UI will be available at:

http://127.0.0.1:8000/docs#/
````
