from src.inventory.service_layer import unit_of_work
from src.inventory.domain import model
from src.inventory.adapters import repository
from src.database.database import get_session


async def get_book_by_id(pk: int, uow: unit_of_work.AbstractUnitOfWork) -> model.BookModel:
    async with uow:
        return await uow.book.get(pk=pk)



# async def get_book_by_id(pk: int) -> model.BookModel:
#     session = await get_session()
#     return await repository.BookRepository(session=session).get(pk=pk)
    # return await uow.book.get(pk=pk)

