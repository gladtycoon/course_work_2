from abc import ABC, abstractmethod


class AbstractFlightAPI(ABC):
    """Абстрактный класс для работы с авиа-API"""

    @abstractmethod
    def get_country_bounding_box(self, country_name: str):
        """Получить границы страны (юг, север, запад, восток)"""
        pass

    @abstractmethod
    def get_aircraft_by_country(self, country_name: str):
        """Получить список самолетов в воздушном пространстве страны"""
        pass
