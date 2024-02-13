import logging

from common.handlers.base import MessageHandler
from ipr_service.schemas import IprRequest
from vlp_service.schemas import VlpRequest

from gateway_service.schemas import CreationTaskSchema, TaskSchema
from gateway_service.services import DbService
from gateway_service.settings import MessageSettings


class TaskService(MessageHandler):
    def __init__(self, db_service: DbService):
        super().__init__()
        self.db_service = db_service
        self.message_settings = MessageSettings()

    async def create_task(self, task_schema: CreationTaskSchema):
        await self.db_service.create_task(task_schema)
        logging.info("it needs to create vlp and ipr tasks")
        vlp_request = self.generate_vlp_request(task_schema)
        ipr_request = self.generate_ipr_request(task_schema)
        self.producer.send_message(
            vlp_request.model_dump_json(),
            self.message_settings.exchange,
            self.message_settings.vlp_queue,
        )
        self.producer.send_message(
            ipr_request.model_dump_json(),
            self.message_settings.exchange,
            self.message_settings.ipr_queue,
        )
        logging.info("the tasks for the ipr and vlp services have been successfully created")

    @staticmethod
    def generate_vlp_request(task_schema: TaskSchema) -> VlpRequest:
        return VlpRequest(
            id=str(task_schema.id),
            inclinometry=task_schema.inclinometry.model_dump(),
            casing=task_schema.casing.model_dump(),
            tubing=task_schema.tubing.model_dump(),
            pvt=task_schema.pvt.model_dump(),
            p_wh=task_schema.p_wh,
            geo_grad=task_schema.geo_grad,
            h_res=task_schema.h_res,
        )

    @staticmethod
    def generate_ipr_request(task_schema: TaskSchema) -> IprRequest:
        return IprRequest(
            id=str(task_schema.id),
            p_res=task_schema.p_res,
            wct=task_schema.pvt.wct,
            pi=task_schema.pi,
            pb=task_schema.pvt.pb,
        )

    async def get_task(self, task_id: str) -> TaskSchema:
        task = await self.db_service.get_task(task_id)
        return TaskSchema.model_validate(task)

    async def update_task(self, task_schema: TaskSchema):
        node_analysis_request = await self.db_service.update_task(task_schema)

        if node_analysis_request:
            logging.info("it needs to create a node analysis task")
            self.producer.send_message(
                node_analysis_request.model_dump_json(),
                self.message_settings.exchange,
                self.message_settings.nodal_analysis_queue,
            )
            logging.info("the nodal analysis task has been successfully created")
