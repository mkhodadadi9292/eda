import abc
from typing import Self
from src.inventory.adapters import repository
from src.database import database


class AbstractUnitOfWork(abc.ABC):
    book: repository.AbstractRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self._commit()

    def collect_new_events(self):
        for product in self.book.seen:
            while product.events:
                yield product.events.pop(0)

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
        self.book = repository.BookRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.aclose()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()