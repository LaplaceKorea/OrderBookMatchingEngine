from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict

import pandas as pd
from pandera.typing import DataFrame

from order_matching.schemas import TradeDataSchema
from order_matching.trade import Trade


class ExecutedTrades:
    def __init__(self, trades: list[Trade] = None) -> None:
        self._trades: dict[pd.Timestamp, list[Trade]] = defaultdict(list)
        if trades:
            self.add(trades=trades)

    @property
    def trades(self) -> list[Trade]:
        trades = list()
        for same_time_trades in self._trades.values():
            trades.extend(same_time_trades)
        return trades

    def add(self, trades: list[Trade]) -> None:
        for trade in trades:
            self._trades[trade.timestamp].append(trade)

    def get(self, timestamp: pd.Timestamp) -> list[Trade]:
        return self._trades[timestamp]

    def to_frame(self) -> DataFrame[TradeDataSchema]:
        trades = self.trades
        if len(trades) == 0:
            return pd.DataFrame()
        else:
            return pd.DataFrame.from_records([asdict(trade) for trade in trades]).assign(
                **{
                    TradeDataSchema.side: lambda df: df[TradeDataSchema.side].astype(str),
                    TradeDataSchema.execution: lambda df: df[TradeDataSchema.execution].astype(str),
                }
            )

    def __add__(self, other: ExecutedTrades) -> ExecutedTrades:
        trades = ExecutedTrades()
        trades.add(trades=self.trades)
        trades.add(trades=other.trades)
        return trades
