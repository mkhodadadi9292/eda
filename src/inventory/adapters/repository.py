import abc
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.inventory.domain import model
from src.inventory.adapters import orm


class AbstractRepository(abc.ABC):
    def __init__(self):
        # self.seen = set()  # type: Set[model.BookModel]
        self.seen = []  # type: List[model.BookModel]

    async def add(self, book: model.BookModel):
        self.seen.append(book)
        return await self._add(book)

    async def get(self, pk) -> model.BookModel:
        book = await self._get(pk=pk)
        if book:
            self.seen.append(book)
        return book

    @abc.abstractmethod
    async def update(self, pk: int, book: model.BookModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> List[model.BookModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _add(self, book: model.BookModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk) -> model.BookModel:
        raise NotImplementedError


class BookRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, book: model.BookModel):
        _book: orm.Book = orm.Book.data_model_to_sqlmodel(book)
        self.session.add(_book)
        await self.session.flush()
        return _book

    async def _get(self, pk) -> model.BookModel:
        statement = select(orm.Book).where(orm.Book.id == pk)
        query_result = await self.session.execute(statement)
        result: orm.Book = query_result.scalars().first()
        return model.BookModel(**result.dict())

    async def get_all(self) -> List[model.BookModel]:
        statement = select(orm.Book)
        query_result = await self.session.execute(statement)
        result: List[orm.Book] = query_result.scalars().all()
        return [model.BookModel(**m.dict()) for m in result]

    async def update(self, pk: int, book: model.BookModel):
        statement = update(orm.Book).where(orm.Book.id == pk).values(**book.dict())
        await self.session.execute(statement)
