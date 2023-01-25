import pandas as pd

from order_matching.order import LimitOrder
from order_matching.orders import Orders
from order_matching.schemas import OrderBookSummarySchema
from order_matching.side import Side
from order_matching.unprocessed_orders import UnprocessedOrders


class TestUnprocessedOrders:
    def test_init(self) -> None:
        unprocessed_orders = UnprocessedOrders()

        assert unprocessed_orders.bids == {}
        assert unprocessed_orders.offers == {}
        assert unprocessed_orders.current_price == float("inf")

    def test_append_with_same_price(self) -> None:
        unprocessed_orders = UnprocessedOrders()

        timestamp = pd.Timestamp.now()
        buy_price, sell_price = 1.2, 1.3
        buy_orders = [
            LimitOrder(side=Side.BUY, price=buy_price, size=size, timestamp=timestamp, order_id=order_id, trader_id="x")
            for size, order_id in zip([12, 65, 98], ["a", "b", "c"])
        ]
        sell_orders = [
            LimitOrder(
                side=Side.SELL, price=sell_price, size=size, timestamp=timestamp, order_id=order_id, trader_id="y"
            )
            for size, order_id in zip([12, 65, 98], ["a", "b", "c"])
        ]
        for order in [*buy_orders, *sell_orders]:
            unprocessed_orders.append(incoming_order=order)

        assert unprocessed_orders.bids == {buy_price: Orders(buy_orders)}
        assert unprocessed_orders.offers == {sell_price: Orders(sell_orders)}
        assert unprocessed_orders.current_price == (buy_price + sell_price) / 2

    def test_append(self) -> None:
        unprocessed_orders = UnprocessedOrders()

        timestamp = pd.Timestamp.now()
        buy_order_first = LimitOrder(
            side=Side.BUY, price=1.2, size=2.3, timestamp=timestamp, order_id="xyz", trader_id="x"
        )
        unprocessed_orders.append(incoming_order=buy_order_first)

        assert unprocessed_orders.bids == {buy_order_first.price: Orders([buy_order_first])}
        assert unprocessed_orders.offers == dict()
        assert unprocessed_orders.current_price == float("inf")

        sell_order_first = LimitOrder(
            side=Side.SELL, price=3.4, size=5.6, timestamp=timestamp, order_id="abc", trader_id="x"
        )
        unprocessed_orders.append(incoming_order=sell_order_first)

        assert unprocessed_orders.bids == {buy_order_first.price: Orders([buy_order_first])}
        assert unprocessed_orders.offers == {sell_order_first.price: Orders([sell_order_first])}
        assert unprocessed_orders.current_price == 2.3

        buy_order_second = LimitOrder(
            side=Side.BUY, price=buy_order_first.price, size=6.7, timestamp=timestamp, order_id="qwe", trader_id="x"
        )
        sell_order_second = LimitOrder(
            side=Side.SELL, price=5.9, size=9.3, timestamp=timestamp, order_id="abc", trader_id="x"
        )
        unprocessed_orders.append(incoming_order=buy_order_second)
        unprocessed_orders.append(incoming_order=sell_order_second)

        assert unprocessed_orders.bids == {buy_order_first.price: Orders([buy_order_first, buy_order_second])}
        assert unprocessed_orders.offers == {
            sell_order_first.price: Orders([sell_order_first]),
            sell_order_second.price: Orders([sell_order_second]),
        }
        assert unprocessed_orders.current_price == 2.3

    def test_cancel(self) -> None:
        unprocessed_orders = UnprocessedOrders()
        buy_order = self._get_sample_orders().orders[0]

        assert unprocessed_orders.bids == dict()

        unprocessed_orders.remove(incoming_order=buy_order)

        assert unprocessed_orders.bids == dict()

        unprocessed_orders.append(incoming_order=buy_order)

        assert unprocessed_orders.bids == {buy_order.price: Orders([buy_order])}

        unprocessed_orders.remove(incoming_order=buy_order)

        assert unprocessed_orders.bids == dict()

    def test_unprocessed_orders_summary(self) -> None:
        unprocessed_orders = UnprocessedOrders()
        for order in self._get_sample_orders():
            unprocessed_orders.append(incoming_order=order)
        summary = unprocessed_orders.summary()

        OrderBookSummarySchema.validate(summary, lazy=True)
        assert summary.index.is_monotonic_increasing
        assert summary[OrderBookSummarySchema.price].is_monotonic_increasing
        assert unprocessed_orders.current_price == 2.3

    def test_order_book_imbalance_one_buy_order(self) -> None:
        unprocessed_orders = UnprocessedOrders()
        buy_orders = [
            LimitOrder(side=Side.BUY, price=1.3, size=38, timestamp=pd.Timestamp.now(), order_id="x", trader_id="x")
        ]
        for order in [*buy_orders]:
            unprocessed_orders.append(incoming_order=order)

        assert unprocessed_orders.get_imbalance(price_range=0.1) == 1

    def test_order_book_imbalance_one_sell_order(self) -> None:
        unprocessed_orders = UnprocessedOrders()
        sell_orders = [
            LimitOrder(side=Side.SELL, price=1.3, size=38, timestamp=pd.Timestamp.now(), order_id="x", trader_id="x")
        ]
        for order in [*sell_orders]:
            unprocessed_orders.append(incoming_order=order)

        assert unprocessed_orders.get_imbalance(price_range=0.1) == -1

    def test_order_book_imbalance_with_equal_orders(self) -> None:
        unprocessed_orders = UnprocessedOrders()
        timestamp = pd.Timestamp.now()
        buy_orders = [LimitOrder(side=Side.BUY, price=1.4, size=10, timestamp=timestamp, order_id="x", trader_id="x")]
        sell_orders = [
            LimitOrder(side=Side.SELL, price=1.6, size=10, timestamp=timestamp, order_id="x", trader_id="y"),
            LimitOrder(side=Side.SELL, price=1.8, size=20, timestamp=timestamp, order_id="x", trader_id="y"),
        ]
        for order in [*buy_orders, *sell_orders]:
            unprocessed_orders.append(incoming_order=order)

        assert unprocessed_orders.get_imbalance(price_range=0.05) == 0
        assert unprocessed_orders.get_imbalance(price_range=0.1) == 0
        assert unprocessed_orders.get_imbalance(price_range=0.2) == 0
        assert unprocessed_orders.get_imbalance(price_range=0.3) == (10 - 20 - 10) / (10 + 20 + 10)

    def test_order_book_imbalance_with_several_orders(self) -> None:
        unprocessed_orders = UnprocessedOrders()
        timestamp = pd.Timestamp.now()
        buy_orders = [
            LimitOrder(side=Side.BUY, price=price, size=size, timestamp=timestamp, order_id="x", trader_id="x")
            for size, price in zip([12, 65, 98], [1.1, 1.3, 1.4])
        ]
        sell_orders = [
            LimitOrder(side=Side.SELL, price=price, size=size, timestamp=timestamp, order_id="x", trader_id="y")
            for size, price in zip([8, 86, 72], [1.5, 1.7, 1.8])
        ]
        for order in [*buy_orders, *sell_orders]:
            unprocessed_orders.append(incoming_order=order)

        assert unprocessed_orders.get_imbalance(price_range=0.1) == (98 - 8) / (98 + 8)
        assert unprocessed_orders.get_imbalance(price_range=0.2) == (65 + 98 - 8) / (65 + 98 + 8)
        assert unprocessed_orders.get_imbalance(price_range=0.3) == (65 + 98 - 8 - 86) / (65 + 98 + 8 + 86)
        assert unprocessed_orders.get_imbalance(price_range=0.4) == (12 + 65 + 98 - 8 - 86 - 72) / (
            12 + 65 + 98 + 8 + 86 + 72
        )

    @staticmethod
    def _get_sample_orders() -> Orders:
        timestamp = pd.Timestamp.now()
        return Orders(
            [
                LimitOrder(side=Side.BUY, price=1.2, size=2.3, timestamp=timestamp, order_id="xyz", trader_id="x"),
                LimitOrder(side=Side.SELL, price=3.4, size=5.6, timestamp=timestamp, order_id="abc", trader_id="x"),
                LimitOrder(side=Side.BUY, price=1.2, size=6.7, timestamp=timestamp, order_id="qwe", trader_id="x"),
                LimitOrder(side=Side.SELL, price=5.9, size=9.3, timestamp=timestamp, order_id="abc", trader_id="x"),
                LimitOrder(side=Side.BUY, price=1.1, size=6.7, timestamp=timestamp, order_id="qwe", trader_id="x"),
            ]
        )
