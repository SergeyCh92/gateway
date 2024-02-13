import uuid
from datetime import datetime

from common.models.oil_data import OilData
from common.models.point import Point
from pydantic import Field

from gateway_service.models import TaskStatus
from gateway_service.schemas import BaseSchema


class TaskSchema(BaseSchema):
    id: str
    status: int = TaskStatus.new
    ipr: OilData | None = None
    vlp: OilData | None = None
    nodal_analysis: list[Point] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Inclinometry(BaseSchema):
    MD: list[float]
    TVD: list[float]


class Casing(BaseSchema):
    d: float


class Tubing(BaseSchema):
    d: float
    h_mes: float


class PVT(BaseSchema):
    wct: float | int
    rp: float | int
    gamma_oil: float | int
    gamma_gas: float | int
    gamma_wat: float | int
    t_res: float | int
    pb: float | int


class CreationTaskSchema(BaseSchema):
    id: str = Field(default_factory=uuid.uuid4)
    status: int = TaskStatus.new
    inclinometry: Inclinometry
    casing: Casing
    tubing: Tubing
    pvt: PVT
    p_wh: float | int
    geo_grad: float | int
    h_res: float
    p_res: float
    pi: float
