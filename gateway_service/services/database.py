from nodal_analysis.schemas import NodeAnalysisRequest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from gateway_service.database.tables import Task
from gateway_service.models import TaskStatus
from gateway_service.schemas import CreationTaskSchema, TaskSchema


class DbService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_schema: CreationTaskSchema):
        query = insert(Task).values(id=task_schema.id, status=task_schema.status)
        await self.session.execute(query)
        await self.session.commit()

    async def get_task(self, task_id: str) -> Task:
        query = select(Task).where(Task.id == task_id)
        raw_task = await self.session.execute(query)
        task = raw_task.scalar()
        return task

    async def update_task(self, task_schema: TaskSchema) -> NodeAnalysisRequest | None:
        node_analysis_request = None
        query = select(Task).where(Task.id == task_schema.id).with_for_update(nowait=False)
        raw_task = await self.session.execute(query)
        task = raw_task.scalar()

        task.status = task_schema.status
        task.ipr = task_schema.ipr.model_dump() if task_schema.ipr else task.ipr
        task.vlp = task_schema.vlp.model_dump() if task_schema.vlp else task.vlp
        task.nodal_analysis = (
            [data.model_dump() for data in task_schema.nodal_analysis]
            if task_schema.nodal_analysis
            else task.nodal_analysis
        )

        if (
            task.vlp
            and task.ipr
            and (task.nodal_analysis is None and task.status != TaskStatus.processed)
        ):
            node_analysis_request = NodeAnalysisRequest(id=str(task.id), ipr=task.ipr, vlp=task.vlp)

        await self.session.commit()
        return node_analysis_request
