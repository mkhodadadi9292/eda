from fastapi import FastAPI, Depends, APIRouter, status
from typing import List
from src.inventory.adapters.orm import Book
from src.inventory.domain.model import BookModel
from src.inventory.service_layer.unit_of_work import SqlAlchemyUnitOfWork, AbstractUnitOfWork, get_uow
from src.inventory.service_layer import service

router = APIRouter(tags=["Inventory"])


@router.post("/books/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def add_book(body: BookModel, uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.add_book(book=body, uow=uow)


@router.put("/books/{pk}", )
async def update_book(body: BookModel, pk: int, uow: AbstractUnitOfWork = Depends(get_uow)):
    await service.update_book(pk=pk, book=body, uow=uow)


@router.get("/books/{pk}", response_model=BookModel)
async def get_book(pk: int = None, uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.get_book_by_id(pk=pk, uow=uow)


@router.get("/books/", response_model=List[BookModel])
async def get_all_books(uow: AbstractUnitOfWork = Depends(get_uow)):
    return await service.get_books(uow=uow)
