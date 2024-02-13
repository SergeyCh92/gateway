from datetime import datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from gateway_service.database.engine import Base


class Task(Base):
    """Содержит информацию о статусе задачи, промежуточные и финальные результаты."""

    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Идентификатор задачи."
    )
    status: Mapped[int] = mapped_column(comment="Статус задачи в цифровом виде.")
    ipr: Mapped[dict] = mapped_column(JSONB, nullable=True, comment="Результат вычисления ipr.")
    vlp: Mapped[dict] = mapped_column(JSONB, nullable=True, comment="Результат вычисления vlp.")
    nodal_analysis: Mapped[dict] = mapped_column(
        JSONB, nullable=True, comment="Результат вычисления узлового анализа."
    )
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow
    )
