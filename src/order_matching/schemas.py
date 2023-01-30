from pandera import Field, SchemaModel
from pandera.typing import DateTime, Series

from order_matching.execution import Execution
from order_matching.side import Side
from order_matching.status import Status


class BaseOrderSchema(SchemaModel):
    side: Series[str] = Field(isin=[Side.BUY.name, Side.SELL.name])
    price: Series[float] = Field(gt=0)
    size: Series[float] = Field(gt=0)


class OrderBookSummarySchema(BaseOrderSchema):
    price: Series[float] = Field(unique=True, gt=0)
    count: Series[int] = Field(ge=0)

    class Config:
        strict = True


class OrderDataSchema(BaseOrderSchema):
    timestamp: Series[DateTime]
    expiration: Series[DateTime] = Field(nullable=True)
    order_id: Series[str]
    trader_id: Series[str]
    execution: Series[str] = Field(isin=[Execution.MARKET.name, Execution.LIMIT.name])
    status: Series[str] = Field(isin=[Status.OPEN.name, Status.CANCEL.name])
    price_number_of_digits: Series[int]

    class Config:
        strict = True


class TradeDataSchema(BaseOrderSchema):
    timestamp: Series[DateTime]
    incoming_order_id: Series[str]
    book_order_id: Series[str]
    trade_id: Series[str]
    execution: Series[str] = Field(isin=[Execution.MARKET.name, Execution.LIMIT.name])

    class Config:
        strict = True
