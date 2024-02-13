import aiohttp
from gateway_service.schemas import TaskSchema


def session_factory(func):
    async def wrapper(*args, **kwargs):
        async with aiohttp.ClientSession() as aio_session:
            result = await func(*args, session=aio_session, **kwargs)
        return result

    return wrapper


class GatewayManager:
    def __init__(self, service_url: str):
        self.service_url: str = service_url

    @session_factory
    async def get_task(
        self, session: aiohttp.ClientSession, task_id: str
    ) -> TaskSchema:
        async with session.get(f"{self.service_url}/tasks/task/{task_id}") as response:
            raw_task = await response.json()
        return TaskSchema.model_validate(raw_task)

    @session_factory
    async def update_task(
        self, session: aiohttp.ClientSession, task_schema: TaskSchema
    ):
        async with session.put(
            f"{self.service_url}/tasks/task", json=task_schema.model_dump()
        ) as response:
            if not response.ok:
                error_text = await response.text()
                raise Exception(f"failed to update task {task_schema.id}: {error_text}")
