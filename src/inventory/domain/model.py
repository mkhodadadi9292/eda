from pydantic import BaseModel
from sqlmodel import SQLModel

class BookModel(SQLModel, table=False):
    title: str
    author: str
    quantity: int

    def increase_quantity(self):
        self.quantity += 1000
        return self.quantity