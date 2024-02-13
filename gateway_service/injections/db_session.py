from gateway_service.database.session import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def inject_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
