from unittest.mock import patch

import pytest

from src.flight_api import APIAdapter


@patch("src.flight_api.requests.get")
def test_get_country_bounding_box(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [{"boundingbox": ["41.0", "83.0", "-141.0", "-52.0"]}]

    api = APIAdapter()
    result = api.get_country_bounding_box("Canada")

    assert result["south"] == 41.0
    assert result["north"] == 83.0
    assert result["west"] == -141.0
    assert result["east"] == -52.0


from unittest.mock import Mock, patch

import pytest

from src.flight_api import APIAdapter


@patch("src.flight_api.requests.get")
def test_get_aircraft_by_country(mock_get):
    # 1. Мокаем первый вызов (get_country_bounding_box)
    mock_response1 = Mock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = [{"boundingbox": ["40", "85", "-140", "-50"]}]

    # 2. Мокаем второй вызов (opensky)
    mock_response2 = Mock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = {
        "states": [["abc123", "AFL123", "Russia", None, None, 10, 20, 10000, False, 250]]
    }

    # 3. Подставляем ответы по порядку
    mock_get.side_effect = [mock_response1, mock_response2]

    api = APIAdapter()
    result = api.get_aircraft_by_country("Russia")

    assert len(result) == 1
    assert result[0][1] == "AFL123"
