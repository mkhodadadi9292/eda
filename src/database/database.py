from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/my_database"

engine = create_async_engine(DATABASE_URL, future=True)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# TODO: Following code is suggested for making sync sessions.
# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(
#         config.get_postgres_uri(),
#         isolation_level="REPEATABLE READ",
#     )
# )


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
