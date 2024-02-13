from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gateway_service.injections import inject_db_session
from gateway_service.services import DbService


async def inject_db_service(session: AsyncSession = Depends(inject_db_session)) -> DbService:
    return DbService(session)
