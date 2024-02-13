import logging

from fastapi import APIRouter, Depends, Response, status

from gateway_service.injections import inject_task_service
from gateway_service.schemas import CreationTaskSchema, TaskSchema
from gateway_service.services import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/task", response_class=Response)
async def create_task(
    task_schema: CreationTaskSchema, task_service: TaskService = Depends(inject_task_service)
):
    logging.info(
        f"the request was received to create a task, params: {task_schema.model_dump_json}"
    )
    await task_service.create_task(task_schema)
    logging.info("the task has been successfully created")
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/task/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str, task_service: TaskService = Depends(inject_task_service)):
    logging.info(f"the task {task_id} was requested")
    task = await task_service.get_task(task_id)
    logging.info(f"the task {task_id} was received")
    return task


@router.put("/task", response_class=Response)
async def update_task(
    task_schema: TaskSchema, task_service: TaskService = Depends(inject_task_service)
):
    logging.info(f"request to update task {task_schema.id}")
    await task_service.update_task(task_schema)
    logging.info(f"task {task_schema.id} updated")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
