from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/my_database"

connect_args = {"server_settings": {"options": "-c timezone=UTC", "timezone": "UTC"}}
engine = create_async_engine(DATABASE_URL, future=True, connect_args=connect_args)

async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
        # await session.commit()
