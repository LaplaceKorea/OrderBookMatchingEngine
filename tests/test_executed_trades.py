import pandas as pd

from order_matching.executed_trades import ExecutedTrades
from order_matching.execution import Execution
from order_matching.schemas import TradeDataSchema
from order_matching.side import Side
from order_matching.trade import Trade


class TestExecutedTrades:
    def test_init(self) -> None:
        executed_trades = ExecutedTrades()

        assert executed_trades.trades == list()

        trades = self._get_sample_trades()
        executed_trades = ExecutedTrades(trades=trades)

        assert executed_trades.trades == trades

    def test_add(self) -> None:
        executed_trades = ExecutedTrades()
        first_trade, second_trade = self._get_sample_trades()
        executed_trades.add(trades=[first_trade])

        assert executed_trades.trades == [first_trade]

        executed_trades.add(trades=[second_trade])

        assert executed_trades.trades == [first_trade, second_trade]

        executed_trades.add(trades=[second_trade, first_trade])

        assert executed_trades.trades == [first_trade, second_trade, second_trade, first_trade]

    def test_to_frame(self) -> None:
        executed_trades = ExecutedTrades()
        first_trade, second_trade = self._get_sample_trades()
        executed_trades.add(trades=[first_trade, second_trade])

        TradeDataSchema.validate(executed_trades.to_frame(), lazy=True)

    def test_dunder_add(self) -> None:
        executed_trades_first = ExecutedTrades()
        first_trade, second_trade = self._get_sample_trades()
        executed_trades_first.add(trades=[first_trade])
        executed_trades_second = ExecutedTrades()
        executed_trades_second.add(trades=[second_trade])
        executed_trades_third = ExecutedTrades()
        executed_trades_third.add(trades=[first_trade])

        assert (executed_trades_first + executed_trades_second + executed_trades_third).trades == [
            first_trade,
            second_trade,
            first_trade,
        ]
        assert executed_trades_first.trades == [first_trade]
        assert executed_trades_second.trades == [second_trade]
        assert executed_trades_third.trades == [first_trade]

    @staticmethod
    def _get_sample_trades() -> list[Trade]:
        return [
            Trade(
                side=Side.SELL,
                price=0.5,
                size=0.9,
                timestamp=pd.Timestamp.now(),
                incoming_order_id="a",
                book_order_id="x",
                execution=Execution.LIMIT,
                trade_id="t",
            ),
            Trade(
                side=Side.BUY,
                price=0.8,
                size=0.4,
                timestamp=pd.Timestamp.now(),
                incoming_order_id="b",
                book_order_id="y",
                execution=Execution.LIMIT,
                trade_id="t",
            ),
        ]
