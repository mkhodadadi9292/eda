from typing import List
from Inventory_service.src.inventory.service_layer import unit_of_work
from Inventory_service.src.inventory.domain import model


async def get_book_by_id(pk: int, uow: unit_of_work.AbstractUnitOfWork) -> model.BookModel:
    async with uow:
        return await uow.book.get(pk=pk)


async def get_books(uow: unit_of_work.AbstractUnitOfWork) -> List[model.BookModel]:
    async with uow:
        return await uow.book.get_all()


async def add_book(book: model.BookModel, uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        inserted_record = await uow.book.add(book)
        await uow.commit()
    return inserted_record

async def update_book(pk: int, book: model.BookModel, uow: unit_of_work.AbstractUnitOfWork):
    async with uow:
        await uow.book.update(pk=pk, book=book)
        await uow.commit()
