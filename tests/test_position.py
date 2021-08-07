import pytest

from src.position import Position


def test_is_position_higher():
    position: Position = Position()
    position.set_purchase_price(120)
    position.set_sell_price(150)
    assert position.is_winner()

