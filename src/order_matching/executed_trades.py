from __future__ import annotations

from dataclasses import asdict

import pandas as pd
from pandera.typing import DataFrame

from order_matching.schemas import TradeDataSchema
from order_matching.trade import Trade


class ExecutedTrades:
    def __init__(self, trades: list[Trade] = None) -> None:
        self.trades: list[Trade] = list() if trades is None else trades

    def add(self, trades: list[Trade]) -> None:
        self.trades.extend(trades)

    def to_frame(self) -> DataFrame[TradeDataSchema]:
        if len(self.trades) == 0:
            return pd.DataFrame()
        else:
            return pd.DataFrame.from_records([asdict(trade) for trade in self.trades]).assign(
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
