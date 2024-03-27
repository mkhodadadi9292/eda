from sqlmodel import SQLModel, Field
# from Inventory_service.src.inventory.domain.model import ProductModel
from ..domain.model import ProductModel



class Product(ProductModel, table=True):
    id: int = Field(primary_key=True)

    @classmethod
    def data_model_to_sqlmodel(cls, obj: ProductModel) -> SQLModel:
        return cls(**obj.dict())
