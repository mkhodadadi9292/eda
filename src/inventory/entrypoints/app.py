# src/app1/app.py

from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.inventory.adapters.orm import Book
from src.inventory.domain.model import BookModel
from src.database.database import get_session

router = APIRouter(tags=["Authentication"])


@router.post("/books/")
async def create_user(body: BookModel, session: AsyncSession = Depends(get_session)):
    book = Book(title=body.title,
                author=body.author,
                quantity=body.quantity)
    session.add(book)
    await session.commit()
    return {"message": "Hello world!!"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
