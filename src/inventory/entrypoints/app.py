# src/app1/app.py

from fastapi import FastAPI, Depends, APIRouter, status
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.inventory.adapters.orm import Book
from src.inventory.domain.model import BookModel
from src.inventory.service_layer.unit_of_work import SqlAlchemyUnitOfWork, AbstractUnitOfWork
from src.database.database import get_session
from src.inventory.service_layer import service
router = APIRouter(tags=["Authentication"])


@router.post("/books/", status_code=status.HTTP_201_CREATED)
async def add_book(body: BookModel, uow: AbstractUnitOfWork = Depends(SqlAlchemyUnitOfWork)):

    # book = Book.data_model_to_sqlmodel(body)
    # book.increase_quantity()
    # session.add(book)
    # await session.commit()
    return {"message": "Book"}

@router.put("/books/{pk}")
async def update_book(body: BookModel, pk: int, session: AsyncSession =Depends(get_session)):
    book = Book.data_model_to_sqlmodel(body)
    pass

@router.get("/books/{pk}", response_model=BookModel)
async def get_book(pk: int = None, uow: AbstractUnitOfWork = Depends(SqlAlchemyUnitOfWork)):
    return await service.get_book_by_id(pk=pk, uow=uow)



@router.get("/books/", response_model=List[BookModel])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    statement = select(Book)
    query_result = await session.execute(statement)
    return query_result.scalars().all()
