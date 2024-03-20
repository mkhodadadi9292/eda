import abc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.inventory.domain import model
from src.inventory.adapters import orm


class AbstractRepository(abc.ABC):
    def __init__(self):
        # self.seen = set()  # type: Set[model.BookModel]
        self.seen = []  # type: List[model.BookModel]

    async def add(self, book: model.BookModel):
        await self._add(book)
        self.seen.append(book)

    async def get(self, pk) -> model.BookModel:
        book = await self._get(pk=pk)
        if book:
            self.seen.append(book)
        return book

    @abc.abstractmethod
    async def _add(self, product: model.BookModel):
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

    async def _get(self, pk):
        statement = select(orm.Book).where(orm.Book.id == pk)
        query_result = await self.session.execute(statement)
        result: orm.Book = query_result.scalars().first()
        return model.BookModel(**result.dict())
