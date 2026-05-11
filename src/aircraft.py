class Aircraft:
    """Класс Aircraft с валидацией и сравнением"""

    def __init__(self, icao24, callsign, origin_country, velocity=None, altitude=None):
        self.icao24 = self._validate_icao24(icao24)
        self.callsign = self._validate_callsign(callsign)
        self.origin_country = self._validate_country(origin_country)
        self.velocity = self._validate_velocity(velocity)
        self.altitude = self._validate_altitude(altitude)

    # ========== ВАЛИДАЦИЯ ==========
    def _validate_icao24(self, value: str):
        """Проверяем по коду ИКАО"""
        if not isinstance(value, str) or len(value) != 6:
            raise ValueError("ICAO24 должен быть строкой из 6 символов")
        return value.upper()

    def _validate_callsign(self, value: str):
        """Проверяем по позывному"""
        return value.strip() if value else "N/A"

    def _validate_country(self, value: str):
        """Проверяем по стране"""
        return value.strip() if value else "Неизвестная страна"

    def _validate_velocity(self, value: int):
        """Проверяем по скорости"""
        if value is None:
            return None
        try:
            v = float(value)
            return round(v, 1) if v >= 0 else None
        except ValueError, TypeError:
            return None

    def _validate_altitude(self, value: int):
        """Проверяем по высоте"""
        if value is None:
            return None
        try:
            a = float(value)
            return round(a, 1) if a >= 0 else 0
        except ValueError, TypeError:
            return None

    # ========== ГЕТТЕРЫ ==========
    @property
    def velocity_kmh(self):
        """Перевод из м/с в км/ч"""
        return self.velocity * 3.6 if self.velocity else None

    # ========== СРАВНЕНИЕ ПО СКОРОСТИ ==========
    def __lt__(self, other):
        """Сравнение объектов класса Aircraft по скорости (lt - меньше чем)"""
        if not isinstance(other, Aircraft):
            return NotImplemented
        if self.velocity is None and other.velocity is None:
            return False
        if self.velocity is None:
            return True
        if other.velocity is None:
            return False
        return self.velocity < other.velocity

    def __gt__(self, other):
        """Сравнение объектов класса Aircraft по скорости (gt - больше чем)"""
        if not isinstance(other, Aircraft):
            return NotImplemented
        if self.velocity is None and other.velocity is None:
            return False
        if self.velocity is None:
            return False
        if other.velocity is None:
            return True
        return self.velocity > other.velocity

    # ========== СРАВНЕНИЕ ПО ВЫСОТЕ ==========
    def altitude_lt(self, other):
        """Сравнение объектов класса Aircraft по высоте (lt - меньше чем)"""
        if not isinstance(other, Aircraft):
            return NotImplemented
        if self.altitude is None and other.altitude is None:
            return False
        if self.altitude is None:
            return True
        if other.altitude is None:
            return False
        return self.altitude < other.altitude

    def altitude_gt(self, other):
        """Сравнение объектов класса Aircraft по высоте (gt - больше чем чем)"""
        if not isinstance(other, Aircraft):
            return NotImplemented
        if self.altitude is None and other.altitude is None:
            return False
        if self.altitude is None:
            return False
        if other.altitude is None:
            return True
        return self.altitude > other.altitude

    # ========== СТРОКОВЫЙ ВЫВОД ==========
    def __str__(self):
        vel = f"{self.velocity} м/с" if self.velocity else "N/A"
        alt = f"{self.altitude} м" if self.altitude else "N/A"
        return f"{self.callsign} ({self.origin_country}) | {vel} | {alt}"
