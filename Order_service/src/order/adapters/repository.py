import abc
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Order_service.src.order.domain import model
from Order_service.src.order.adapters import orm


class AbstractRepository(abc.ABC):
    def __init__(self):
        # self.seen = set()  # type: Set[model.OrderingModel]
        self.seen = []  # type: List[model.OrderingModel]

    async def add(self, new_order: model.OrderingModel):
        self.seen.append(new_order)
        return await self._add(new_order)

    async def get(self, pk) -> model.OrderingModel:
        order = await self._get(pk=pk)
        if order:
            self.seen.append(order)
        return order

    #
    # @abc.abstractmethod
    # async def update(self, pk: int, order: model.OrderingModel):
    #     raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> List[model.OrderingModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _add(self, new_order: model.OrderingModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk) -> model.OrderingModel:
        raise NotImplementedError


class OrderRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, new_order: model.OrderingModel):
        _new_order: orm.Ordering = orm.Ordering.data_model_to_sqlmodel(new_order)
        self.session.add(_new_order)
        await self.session.flush()
        return _new_order

    async def _get(self, pk) -> model.OrderingModel:
        statement = select(orm.Ordering).where(orm.Ordering.id == pk)
        query_result = await self.session.execute(statement)
        result: orm.Ordering = query_result.scalars().first()
        return model.OrderingModel(**result.dict())

    async def get_all(self) -> List[model.OrderingModel]:
        statement = select(orm.Ordering)
        query_result = await self.session.execute(statement)
        result: List[orm.Ordering] = query_result.scalars().all()
        return [model.OrderingModel(**m.dict()) for m in result]
