from celery import Celery
import time

# Create Celery instance
app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

# Optional configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tokyo",
    enable_utc=True,
)


@app.task
def add(x, y):
    """Simple task that adds two numbers"""
    return x + y


@app.task
def long_task(seconds):
    """Task that simulates a long-running process"""
    time.sleep(seconds)
    return f"Task completed after {seconds} seconds"


@app.task
def process_data(data):
    """Task that processes a list of numbers"""
    result = sum(data)
    return f"Processed {len(data)} items. Sum: {result}"
