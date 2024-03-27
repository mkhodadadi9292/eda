import abc
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from Inventory_service.src.inventory.domain import model
from Inventory_service.src.inventory.adapters import orm


class AbstractRepository(abc.ABC):
    def __init__(self):
        # self.seen = set()  # type: Set[model.ProductModel]
        self.seen = []  # type: List[model.ProductModel]

    async def add(self, book: model.ProductModel):
        self.seen.append(book)
        return await self._add(book)

    async def get(self, pk) -> model.ProductModel:
        book = await self._get(pk=pk)
        if book:
            self.seen.append(book)
        return book

    @abc.abstractmethod
    async def update(self, pk: int, book: model.ProductModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> List[model.ProductModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _add(self, book: model.ProductModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk) -> model.ProductModel:
        raise NotImplementedError


class BookRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, book: model.ProductModel):
        _book: orm.Product = orm.Product.data_model_to_sqlmodel(book)
        self.session.add(_book)
        await self.session.flush()
        return _book

    async def _get(self, pk) -> model.ProductModel:
        statement = select(orm.Product).where(orm.Product.id == pk)
        query_result = await self.session.execute(statement)
        result: orm.Product = query_result.scalars().first()
        return model.ProductModel(**result.dict())

    async def get_all(self) -> List[model.ProductModel]:
        statement = select(orm.Product)
        query_result = await self.session.execute(statement)
        result: List[orm.Product] = query_result.scalars().all()
        return [model.ProductModel(**m.dict()) for m in result]

    async def update(self, pk: int, book: model.ProductModel):
        statement = update(orm.Product).where(orm.Product.id == pk).values(**book.dict())
        await self.session.execute(statement)
