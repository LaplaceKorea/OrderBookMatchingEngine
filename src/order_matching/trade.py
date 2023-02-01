from dataclasses import dataclass

import pandas as pd

from order_matching.execution import Execution
from order_matching.side import Side


@dataclass(kw_only=True)
class Trade:
    """Single trade storage class."""

    side: Side
    price: float
    size: float
    incoming_order_id: str
    book_order_id: str
    execution: Execution
    trade_id: str
    timestamp: pd.Timestamp = None
