from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/my_database"

engine = create_async_engine(DATABASE_URL, future=True)

"""
    If the expire_on_commit parameter is set to True, it means that objects in the session will be expired (marked as "stale")
    after a commit operation. Here's what would happen:

    Expiration of Objects:
        After committing changes to the database, SQLAlchemy will mark all objects in the session as "expired."
        Expired objects are essentially detached from the session, and accessing their attributes or relationships 
        will trigger a lazy-load operation to reload their state from the database.

    Memory Management:
        Expiring objects after commit helps manage memory efficiently by releasing resources associated with objects 
        that are no longer needed in their current state.
        This can be beneficial in scenarios where large numbers of objects are loaded into memory during a session, 
        and you want to ensure that memory usage is optimized.

    Consistency:
        Expiring objects after commit helps maintain consistency between the state of objects in the session and
         the state of the corresponding rows in the database.
        This ensures that subsequent operations on objects reflect the most up-to-date data from the database.

    In summary, setting expire_on_commit to True ensures that objects in the session are expired after committing changes to
     the database. This helps manage memory efficiently and ensures consistency between the session and the database state.
      However, it may result in additional overhead due to lazy-loading operations when accessing expired objects.
"""
async_session_maker = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


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
