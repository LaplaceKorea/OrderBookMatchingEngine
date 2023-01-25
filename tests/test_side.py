from order_matching.side import Side


def test_side() -> None:
    assert Side.SELL > Side.BUY
    assert str(Side.SELL) == Side.SELL.name
