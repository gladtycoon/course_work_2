import pytest

from src.aircraft import Aircraft


def test_aircraft_creation():
    plane = Aircraft("abc123", "AFL123", "Russia", 250.0, 10000)

    assert plane.icao24 == "ABC123"  # проверка uppercase
    assert plane.callsign == "AFL123"
    assert plane.origin_country == "Russia"
    assert plane.velocity == 250.0
    assert plane.altitude == 10000


def test_aircraft_validation():
    # Неверный ICAO24
    with pytest.raises(ValueError):
        Aircraft("abc", "AFL123", "Russia")

    # Отрицательная скорость → None
    plane = Aircraft("abc123", "AFL123", "Russia", -100, 10000)
    assert plane.velocity is None

    # Отрицательная высота → 0
    plane = Aircraft("abc123", "AFL123", "Russia", 250, -500)
    assert plane.altitude == 0


def test_aircraft_comparison():
    slow = Aircraft("aaa111", "SLOW", "US", 100, 5000)
    fast = Aircraft("bbb222", "FAST", "US", 300, 10000)

    # Сравнение по скорости
    assert slow < fast
    assert fast > slow

    # Сравнение по высоте
    assert slow.altitude_lt(fast)
    assert fast.altitude_gt(slow)
