# Order Book Matching Engine

![pytest](https://github.com/chintai-platform/OrderBookMatchingEngine/actions/workflows/workflow.yaml/badge.svg)
[![!pypi](https://img.shields.io/pypi/v/order-matching)](https://pypi.org/project/order-matching/)
[![!python-versions](https://img.shields.io/pypi/pyversions/order-matching)](https://pypi.org/project/order-matching/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Install

```shell
pip install order-matching
```

## Usage

```python
>>> import pandas as pd

>>> from order_matching.matching_engine import MatchingEngine
>>> from order_matching.order import LimitOrder
>>> from order_matching.side import Side
>>> from order_matching.orders import Orders

>>> matching_engine = MatchingEngine(seed=123)
>>> timestamp = pd.Timestamp("2023-01-01")
>>> transaction_timestamp = timestamp + pd.Timedelta(1, unit="D")
>>> buy_order = LimitOrder(side=Side.BUY, price=1.2, size=2.3, timestamp=timestamp, order_id="a", trader_id="x")
>>> sell_order = LimitOrder(side=Side.SELL, price=0.8, size=1.6, timestamp=timestamp, order_id="b", trader_id="y")
>>> executed_trades = matching_engine.match(orders=Orders([buy_order, sell_order]), timestamp=transaction_timestamp)

>>> print(executed_trades.trades)
[Trade(side=SELL, price=1.2, size=1.6, incoming_order_id='b', book_order_id='a', execution=LIMIT, trade_id='c4da537c-1651-4dae-8486-7db30d67b366', timestamp=Timestamp('2023-01-02 00:00:00'))]

```

## Contribute

Create a virtual environment and activate it:
```shell
python -m venv venv
source venv/bin/activate
```
Install development dependencies:
```shell
pip install -e ".[dev]"
```
and use pre-commit to make sure that your code is formatted using [black](https://github.com/PyCQA/isort) and [isort](https://pycqa.github.io/isort/index.html) automatically:
```shell
pre-commit install
```
Run tests:
```shell
pip install -e ".[test]"
pytest
```
Build and serve documentation website:
```shell
pip install -e ".[doc]"
mkdocs serve
```
