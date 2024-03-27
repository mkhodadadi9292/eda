import abc
from typing import Self
from Order_service.src.order.adapters import repository
from Order_service.src.database import database


class AbstractUnitOfWork(abc.ABC):
    order: repository.AbstractRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.rollback()

    async def commit(self):
        await self._commit()

    def collect_new_events(self):
        for _order in self.order.seen:
            while _order.events:
                yield _order.events.pop(0)

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=database.get_session):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = await self.session_factory()  # type: Session
        self.order = repository.OrderRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow():
    async with SqlAlchemyUnitOfWork() as uow:
        yield uow
