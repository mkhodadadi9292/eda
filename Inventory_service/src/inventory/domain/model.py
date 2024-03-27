from pydantic import BaseModel
from sqlmodel import SQLModel




class ProductModel(SQLModel, table=False):
    uuid: str
    description: str
    quantity: int
    status: str
    # products: list[ProductModel] = []

    # uuid: uuid_pkg.UUID = Field(
    #     default_factory=uuid_pkg.uuid4,
    #     primary_key=True,
    #     index=True,
    #     nullable=False,
    # )

    def increase_quantity(self):
        self.quantity += 1000
        return self.quantity


