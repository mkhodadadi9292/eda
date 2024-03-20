from sqlmodel import SQLModel, Field
from src.inventory.domain.model import BookModel

# class Book(SQLModel, table=True):
#     id: int = Field(primary_key=True)
#     title: str = Field(sa_column_kwargs={"nullable": False})
#     author: str = Field(sa_column_kwargs={"nullable": False})
#     quantity: int = Field(sa_column_kwargs={"nullable": False})


class Book(BookModel, table=True):
    id: int = Field(primary_key=True)

    @classmethod
    def data_model_to_sqlmodel(cls, obj: BookModel) -> SQLModel:
        return cls(**obj.dict())
