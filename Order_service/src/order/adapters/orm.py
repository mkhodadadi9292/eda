from ..domain.model import OrderingModel
from sqlmodel import SQLModel, Field


class Ordering(OrderingModel, table=True):
    id: int = Field(primary_key=True)

    @classmethod
    def data_model_to_sqlmodel(cls, obj: OrderingModel) -> SQLModel:
        return cls(**obj.dict())