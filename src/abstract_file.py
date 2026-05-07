from abc import ABC, abstractmethod


class AbstractFileManager(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_aircraft(self, aircraft):
        """Добавить самолет в файл"""
        pass

    @abstractmethod
    def get_aircraft(self, callsign=None, country=None):
        """Получить самолеты по критериям (позывной или страна)"""
        pass

    @abstractmethod
    def delete_aircraft(self, callsign):
        """Удалить самолет по позывному"""
        pass
