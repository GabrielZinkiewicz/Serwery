# Robert Synoczek, 302922
from typing import Optional, List, Union
from abc import ABC, abstractmethod
import re
import operator


class Product:
    def __init__(self, name: str, price: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__name = name
        self.__price = price

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price


class TooManyProductsFoundError(Exception):
    """Raised when too many products are found"""
    def __init__(self, num_of_objects_found: int = 0):
        message = "Too many products found. Number of Products: {}".format(num_of_objects_found)
        super().__init__(message)


class ServerInterface(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def products(self):
        pass

    @abstractmethod
    def get_entries(self, n_letters: int):
        pass


class ListServer(ServerInterface):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__products = products

    @property
    def products(self):
        return self.__products

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        final_product_list = []

        for pro in self.__products:
            parts = re.match('([a-zA-Z]+)([0-9]+)', pro.name)
            if ((len(parts.groups()[0])) == n_letters) and (2 <= (len(parts.groups()[1])) <= 3):
                final_product_list.append(pro)

        product_list_length = len(final_product_list)
        if product_list_length > ListServer.n_max_returned_entries:
            raise TooManyProductsFoundError(product_list_length)

        final_product_list.sort(key=operator.attrgetter('price'))

        return final_product_list


class MapServer(ServerInterface):
    def __init__(self, products: List, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__products = dict(zip([i.name for i in products], products))

    @property
    def products(self):
        return self.__products

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        final_product_list = []

        for pro in self.__products.values():
            parts = re.match("([a-zA-Z]+)([0-9]+)", pro.name)
            if ((len(parts.groups()[0])) == n_letters) and (2 <= (len(parts.groups()[1])) <= 3):
                final_product_list.append(pro)

        product_list_length = len(final_product_list)
        if product_list_length > MapServer.n_max_returned_entries:
            raise TooManyProductsFoundError(product_list_length)

        final_product_list.sort(key=operator.attrgetter('price'))

        return final_product_list


class Client:
    def __init__(self, server: Union[ListServer, MapServer]):
        self.__server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            chosen_products = self.__server.get_entries(n_letters)
            if len(chosen_products) == 0:
                return None
            total_price = sum([pro.price for pro in chosen_products])
            return total_price
        except TooManyProductsFoundError:
            return None

# Robert Synoczek, 302922