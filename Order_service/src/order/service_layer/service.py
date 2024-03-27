from typing import List
from Order_service.src.order.service_layer import unit_of_work
from Order_service.src.order.domain import model


async def get_order_by_id(pk: int, uow: unit_of_work.AbstractUnitOfWork) -> model.OrderingModel:
    async with uow:
        return await uow.order.get(pk=pk)


async def get_orders(uow: unit_of_work.AbstractUnitOfWork) -> List[model.OrderingModel]:
    async with uow:
        return await uow.order.get_all()


async def add_new_order(new_order: model.OrderingModel, uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        inserted_record = await uow.order.add(new_order)
        await uow.commit()
    return inserted_record

# async def update_order(pk: int, order: model.OrderingModel, uow: unit_of_work.AbstractUnitOfWork):
#     async with uow:
#         await uow.order.update(pk=pk, order=order)
#         await uow.commit()
