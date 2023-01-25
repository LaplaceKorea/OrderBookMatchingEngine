# Order Book Matching Engine

The project is hosted on [GitHub](https://github.com/chintai-platform/OrderBookMatchingEngine).

## Contribute

Create a virtual environment and activate it:
```shell
python -m venv venv
source venv/bin/activate
```
Install development dependencies:
```shell
pip install -e .[dev]
```
and use pre-commit to make sure that your code is formatted using [black](https://github.com/PyCQA/isort) and [isort](https://pycqa.github.io/isort/index.html) automatically:
```shell
pre-commit install
```
Run tests:
```shell
pip install -e .[test]
pytest
```
