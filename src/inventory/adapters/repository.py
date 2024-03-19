import abc
from src.inventory.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Product]

    def add(self, product: model.BookModel):
        self._add(product)
        self.seen.add(product)

    def get(self, sku) -> model.BookModel:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product: model.BookModel):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.BookModel:
        raise NotImplementedError
