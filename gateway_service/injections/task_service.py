from fastapi import Depends

from gateway_service.injections import inject_db_service
from gateway_service.services import DbService, TaskService


async def inject_task_service(db_service: DbService = Depends(inject_db_service)) -> TaskService:
    return TaskService(db_service)
