from fastapi import Depends, APIRouter, status
from typing import List
from Order_service.src.order.adapters.orm import Ordering
from Order_service.src.order.domain.model import OrderingModel
from Order_service.src.order.service_layer.unit_of_work import AbstractUnitOfWork, get_uow
from Order_service.src.order.service_layer import service

router = APIRouter(tags=["Order Service"])


@router.post("/orders/", status_code=status.HTTP_201_CREATED, response_model=Ordering)
async def add_new_order(body: OrderingModel, uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.add_new_order(new_order=body, uow=uow)

#
# @router.put("/orders/{pk}", )
# async def update_book(body: OrderingModel, pk: int, uow: AbstractUnitOfWork = Depends(get_uow)):
#     await service.update_order(pk=pk, book=body, uow=uow)


@router.get("/orders/{pk}", response_model=OrderingModel)
async def get_book(pk: int = None, uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.get_order_by_id(pk=pk, uow=uow)


@router.get("/orders/", response_model=List[OrderingModel])
async def get_all_books(uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.get_orders(uow=uow)
