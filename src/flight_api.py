import requests

from src.abstract_api import AbstractFlightAPI


class APIAdapter(AbstractFlightAPI):
    """Класс для работы с Nominatim и OpenSky API"""

    def __init__(self):
        # URL API
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.headers = {"User-Agent": "test-app/1.0"}  # нужно по условию

    def get_country_bounding_box(self, country_name: str):
        """Получает границы страны через Nominatim API"""
        params = {
            "q": country_name,  # название страны
            "format": "json",  # формат ответа
            "limit": 1,  # берем первый результат
        }

        response = requests.get(self.nominatim_url, params=params, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code}")

        data = response.json()

        # Проверяем, что нашлась страна
        if not data:
            raise Exception(f"Страна '{country_name}' не найдена")

        # Достаем bounding box
        boundingbox = data[0].get("boundingbox")

        if not boundingbox or len(boundingbox) != 4:
            raise Exception(f"Нет координат для страны '{country_name}'")

        # Преобразуем строки в числа и возвращаем словарь
        return {
            "south": float(boundingbox[0]),  # юг
            "north": float(boundingbox[1]),  # север
            "west": float(boundingbox[2]),  # запад
            "east": float(boundingbox[3]),  # восток
        }

    def get_aircraft_by_country(self, country_name: str):
        """Получает список самолетов в воздушном пространстве страны.
        Возвращает список самолетов в формате OpenSky API"""
        # Шаг 1: получаем границы страны
        coordinates = self.get_country_bounding_box(country_name)

        # Шаг 2: формируем параметры запроса к OpenSky
        params = {
            "lamin": coordinates["south"],  # юг
            "lamax": coordinates["north"],  # север
            "lomin": coordinates["west"],  # запад
            "lomax": coordinates["east"],  # восток
        }

        # Шаг 3: отправляем запрос к OpenSky
        response = requests.get(self.opensky_url, params=params)

        if response.status_code != 200:
            raise Exception(f"Ошибка OpenSky API: {response.status_code}")

        # Шаг 4: возвращаем данные
        data = response.json()

        # data['states'] содержит список самолетов или None
        return data.get("states", [])
