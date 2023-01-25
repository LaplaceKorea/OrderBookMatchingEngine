from __future__ import annotations

from dataclasses import asdict
from typing import Generator, Iterator, Sequence

import pandas as pd
from pandera.typing import DataFrame

from order_matching.order import Order
from order_matching.schemas import OrderDataSchema


class Orders:
    def __init__(self, orders: Sequence[Order] = None) -> None:
        self.orders = list() if orders is None else list(orders)
        self._sort_orders_inplace()

    def add(self, orders: list[Order]) -> None:
        self.orders.extend(orders)
        self._sort_orders_inplace()

    def dequeue(self) -> Order:
        return self.orders.pop(0)

    def remove(self, orders: list[Order]) -> None:
        for order_to_remove in orders:
            if order_to_remove.order_id in self._order_ids:
                self.orders.remove(self._get_order(order_id=order_to_remove.order_id))

    def to_frame(self) -> DataFrame[OrderDataSchema]:
        if len(self.orders) == 0:
            return pd.DataFrame()
        else:
            return pd.DataFrame.from_records([asdict(order) for order in self.orders]).assign(
                **{
                    OrderDataSchema.side: lambda df: df[OrderDataSchema.side].astype(str),
                    OrderDataSchema.execution: lambda df: df[OrderDataSchema.execution].astype(str),
                    OrderDataSchema.status: lambda df: df[OrderDataSchema.status].astype(str),
                }
            )

    @property
    def is_empty(self) -> bool:
        return len(self.orders) == 0

    def __add__(self, other: Orders) -> Orders:
        orders = Orders()
        orders.add(orders=self.orders)
        orders.add(orders=other.orders)
        return orders

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Orders):
            return NotImplemented
        else:
            return self.orders == other.orders

    def __iter__(self) -> Iterator[Order]:
        return iter(self.orders)

    def __next__(self) -> Generator[Order, None, None]:
        yield next(self.__iter__())

    def __len__(self) -> int:
        return len(self.orders)

    def _sort_orders_inplace(self) -> None:
        self.orders.sort(key=lambda order: order.timestamp)

    @property
    def _order_ids(self) -> list[str]:
        return [order.order_id for order in self.orders]

    def _get_order(self, order_id: str) -> Order:
        orders = [order for order in self.orders if order.order_id == order_id]
        assert len(orders) <= 1
        return orders[0]
