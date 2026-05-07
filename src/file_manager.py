import json
import os

from .abstract_file import AbstractFileManager


class JSONFileManager(AbstractFileManager):
    """Сохраняет самолеты в JSON-файл"""

    def __init__(self, filename="top_aircrafts.json"):
        self.filename = filename
        if not os.path.exists(filename):
            self._save([])

    def _load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_aircraft(self, aircraft):
        """Добавляет самолет (словарь) в файл"""
        data = self._load()
        data.append(aircraft)
        self._save(data)

    def get_aircraft(self, callsign=None, country=None):
        """Возвращает список самолетов,
        отфильтрованных по callsign или country"""
        data = self._load()
        result = []
        for ac in data:
            if callsign and ac.get("callsign") == callsign:
                result.append(ac)
            elif country and ac.get("origin_country") == country:
                result.append(ac)
        return result

    def delete_aircraft(self, callsign):
        """Удаляет самолет по позывному"""
        data = self._load()
        data = [ac for ac in data if ac.get("callsign") != callsign]
        self._save(data)
