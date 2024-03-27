from fastapi import Depends, APIRouter, status
from typing import List
from Inventory_service.src.inventory.adapters.orm import Product
from Inventory_service.src.inventory.domain.model import ProductModel
from Inventory_service.src.inventory.service_layer.unit_of_work import AbstractUnitOfWork, get_uow
from Inventory_service.src.inventory.service_layer import service

router = APIRouter(tags=["Inventory Service"])


@router.post("/books/", status_code=status.HTTP_201_CREATED, response_model=Product)
async def add_book(body: ProductModel, uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.add_book(book=body, uow=uow)


@router.put("/books/{pk}", )
async def update_book(body: ProductModel, pk: int, uow: AbstractUnitOfWork = Depends(get_uow)):
    await service.update_book(pk=pk, book=body, uow=uow)


@router.get("/books/{pk}", response_model=ProductModel)
async def get_book(pk: int = None, uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.get_book_by_id(pk=pk, uow=uow)


@router.get("/books/", response_model=List[ProductModel])
async def get_all_books(uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.get_books(uow=uow)
