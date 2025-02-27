# Celery with Python and FastAPI Docker Compose Environment

This is a simple example of a Celery setup with Python 3.12, FastAPI, and Redis as the message broker.

<img width="935" alt="image" src="https://github.com/user-attachments/assets/c47a2f9c-3955-4205-8b03-5a788578a01c" />

## Project Structure

- `docker-compose.yml` - Docker Compose configuration
- `Dockerfile` - Python application image definition
- `requirements.txt` - Python dependencies
- `tasks.py` - Celery tasks definition
- `app.py` - Example application that submits Celery tasks directly
- `api.py` - FastAPI application for submitting tasks via REST API
- `static/index.html` - Web interface for interacting with the FastAPI endpoints

## How to Run

1. Start the Docker Compose environment:

```bash
docker compose up
```

2. You should see logs from:
   - The Redis service starting up
   - The Celery worker initializing
   - The Python application submitting tasks
   - The FastAPI application starting
   - The Celery worker processing tasks

3. Access the web interface at http://localhost:8000

4. You can also interact with the API directly:
   - API documentation: http://localhost:8000/docs
   - Submit a task: `POST /tasks/add`, `POST /tasks/long`, or `POST /tasks/process`
   - Check task status: `GET /tasks/{task_id}`
   - Revoke a task: `DELETE /tasks/{task_id}`

5. To stop the environment, press `Ctrl+C` or run:

```bash
docker compose down
```

## Understanding the Example

This example demonstrates three types of Celery tasks:

1. **Simple Addition Task**: A basic task that adds two numbers and returns the result immediately.
2. **Long Running Task**: A task that simulates a time-consuming operation by sleeping for a specified number of seconds.
3. **Data Processing Task**: A task that processes a list of numbers by calculating their sum.

There are two ways to submit tasks:

1. **Direct Python Application**: The `app.py` script submits tasks directly to Celery and waits for results.
2. **FastAPI REST API**: The `api.py` application provides REST endpoints for submitting tasks and checking their status.
   - The web interface in `static/index.html` demonstrates how to use these endpoints from a browser.

## Customizing

To add your own tasks:
1. Add new task functions to `tasks.py`
2. Modify `app.py` to submit your custom tasks directly
3. Add new endpoints to `api.py` for your custom tasks
4. Update the web interface in `static/index.html` to support your new tasks

## Scaling Workers

To scale the number of Celery workers:

```bash
docker compose up -d --scale worker=3
```

This will start 3 worker containers to process tasks in parallel.

## API Documentation

The FastAPI application includes automatic API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These pages provide interactive documentation for all available endpoints.
