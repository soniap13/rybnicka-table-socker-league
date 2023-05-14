from utils import is_float


def test_is_float():
    assert is_float('0')
    assert is_float('1.25')
    assert is_float('123.352492')
    assert not is_float('anythining')
    assert not is_float('1.25anythining')
    assert not is_float('anythining567')
    assert not is_float('123.35v2492')
