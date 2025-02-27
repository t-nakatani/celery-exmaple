# Celery with Python Docker Compose Environment

This is a simple example of a Celery setup with Python 3.12 and Redis as the message broker.

## Project Structure

- `docker-compose.yml` - Docker Compose configuration
- `Dockerfile` - Python application image definition
- `requirements.txt` - Python dependencies
- `tasks.py` - Celery tasks definition
- `app.py` - Example application that submits Celery tasks

## How to Run

1. Start the Docker Compose environment:

```bash
docker-compose up
```

2. You should see logs from:
   - The Redis service starting up
   - The Celery worker initializing
   - The Python application submitting tasks
   - The Celery worker processing tasks

3. To stop the environment, press `Ctrl+C` or run:

```bash
docker-compose down
```

## Understanding the Example

This example demonstrates three types of Celery tasks:

1. **Simple Addition Task**: A basic task that adds two numbers and returns the result immediately.
2. **Long Running Task**: A task that simulates a time-consuming operation by sleeping for a specified number of seconds.
3. **Data Processing Task**: A task that processes a list of numbers by calculating their sum.

The application submits these tasks to the Celery worker and waits for the results of the first and third tasks, while allowing the second task to run in the background.

## Customizing

To add your own tasks:
1. Add new task functions to `tasks.py`
2. Modify `app.py` to submit your custom tasks

## Scaling Workers

To scale the number of Celery workers:

```bash
docker-compose up -d --scale worker=3
```

This will start 3 worker containers to process tasks in parallel.
