from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import List, Optional, Any, Dict
import uvicorn

# Import our Celery tasks
from tasks import add, long_task, process_data

app = FastAPI(title="Celery FastAPI Example", description="Example of using Celery with FastAPI")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define request models
class AddTaskRequest(BaseModel):
    x: int
    y: int


class LongTaskRequest(BaseModel):
    seconds: int


class ProcessDataRequest(BaseModel):
    data: List[int]


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Redirect to the static HTML page
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/api")
async def read_api_root():
    """
    API root endpoint
    """
    return {"message": "Celery FastAPI Example API"}


@app.post("/tasks/add", response_model=TaskResponse)
async def create_add_task(request: AddTaskRequest):
    """
    Submit an addition task to Celery
    """
    # Submit the task to Celery
    task = add.delay(request.x, request.y)

    return {"task_id": task.id, "status": "PENDING", "result": None}


@app.post("/tasks/long", response_model=TaskResponse)
async def create_long_task(request: LongTaskRequest):
    """
    Submit a long-running task to Celery
    """
    # Submit the task to Celery
    task = long_task.delay(request.seconds)

    return {"task_id": task.id, "status": "PENDING", "result": None}


@app.post("/tasks/process", response_model=TaskResponse)
async def create_process_task(request: ProcessDataRequest):
    """
    Submit a data processing task to Celery
    """
    # Submit the task to Celery
    task = process_data.delay(request.data)

    return {"task_id": task.id, "status": "PENDING", "result": None}


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """
    Get the status of a task by its ID
    """
    # Get the task result from Celery
    task_result = AsyncResult(task_id)

    # Check if the task exists
    if not task_result:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    # Prepare the response
    response = {"task_id": task_id, "status": task_result.status}

    # Add the result if the task is ready
    if task_result.ready():
        if task_result.successful():
            response["result"] = task_result.get()
        else:
            # If the task failed, get the exception info
            response["result"] = str(task_result.result)

    return response


@app.delete("/tasks/{task_id}")
async def revoke_task(task_id: str):
    """
    Revoke a task by its ID
    """
    # Get the task result from Celery
    task_result = AsyncResult(task_id)

    # Check if the task exists
    if not task_result:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    # Revoke the task
    task_result.revoke(terminate=True)

    return {"message": f"Task {task_id} has been revoked"}


# Run the FastAPI application with uvicorn when this file is executed directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
