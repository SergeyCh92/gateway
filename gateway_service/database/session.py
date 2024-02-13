from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker
from sqlalchemy.orm import scoped_session, sessionmaker

from gateway_service.database.engine import engine

# SessionLocal = scoped_session(
#     sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# )

# SessionLocal = async_scoped_session(
#     async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# )

SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
