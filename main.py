from src.aircraft import Aircraft
from src.file_manager import JSONFileManager
from src.flight_api import APIAdapter

api = APIAdapter()
file_manager = JSONFileManager()


def filter_aircrafts(aircrafts, filter_words):
    if not filter_words:
        return aircrafts
    result = []
    for plane in aircrafts:
        country = plane[2]
        for word in filter_words:
            if word.lower() in country.lower():
                result.append(plane)
                break
    return result


def get_aircrafts_by_altitude(aircrafts, altitude_range):
    if not altitude_range:
        return aircrafts
    try:
        parts = altitude_range.split("-")
        if len(parts) != 2:
            return aircrafts
        min_alt = float(parts[0].strip())
        max_alt = float(parts[1].strip())
        result = []
        for plane in aircrafts:
            alt = plane[7]
            if alt is not None and min_alt <= alt <= max_alt:
                result.append(plane)
        return result
    except:
        return aircrafts


def sort_aircrafts(aircrafts):
    return sorted(aircrafts, key=lambda x: x[7] if x[7] else 0, reverse=True)


def get_top_aircrafts(aircrafts, top_n):
    return aircrafts[:top_n]


def print_aircrafts(aircrafts):
    if not aircrafts:
        print("Нет самолетов")
        return
    print("\n" + "=" * 60)
    for plane in aircrafts:
        callsign = plane[1] if plane[1] else "N/A"
        country = plane[2]
        altitude = plane[7] if plane[7] else "N/A"
        velocity = plane[9] if plane[9] else "N/A"
        print(f"{callsign} | {country} | {altitude} м | {velocity} м/с")


def user_interaction():
    country = input("Введите страну: ")
    top_n = int(input("Топ N по высоте: "))
    filter_words = input("Фильтр по стране регистрации (через пробел): ").split()
    altitude_range = input("Диапазон высот (например 10000-50000): ")

    aircrafts = api.get_aircraft_by_country(country)
    print(f"\nНайдено: {len(aircrafts)}")

    aircrafts = filter_aircrafts(aircrafts, filter_words)
    aircrafts = get_aircrafts_by_altitude(aircrafts, altitude_range)
    aircrafts = sort_aircrafts(aircrafts)
    top_aircrafts = get_top_aircrafts(aircrafts, top_n)

    print_aircrafts(top_aircrafts)

    # Сохраняем в JSON
    manager = JSONFileManager("top_aircrafts.json")
    for p in top_aircrafts:
        plane_dict = {"callsign": p[1], "origin_country": p[2], "altitude": p[7], "velocity": p[9]}
        manager.add_aircraft(plane_dict)
    print(f"Сохранено в top_aircrafts.json")


if __name__ == "__main__":
    user_interaction()
