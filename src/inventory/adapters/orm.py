from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(sa_column_kwargs={"nullable": False})
    author: str = Field(sa_column_kwargs={"nullable": False})
    quantity: int = Field(sa_column_kwargs={"nullable": False})
