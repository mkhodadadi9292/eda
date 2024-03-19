import abc
from src.inventory.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.BookModel]

    async def add(self, product: model.BookModel):
        await self._add(product)
        self.seen.add(product)

    async def get(self, pk) -> model.BookModel:
        book = await self._get(pk=pk)
        if book:
            self.seen.add(book)
        return book

    @abc.abstractmethod
    async def _add(self, product: model.BookModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk) -> model.BookModel:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def _add(self, book):
        await self.session.add(book)

    async def _get(self, pk):
        #TODO: following is wrong, it should be fixed.
        return await self.session.query(model.BookModel).filter_by(pk=pk).first()

