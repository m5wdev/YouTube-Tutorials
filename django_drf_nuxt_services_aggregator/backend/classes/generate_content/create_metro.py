from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.cities.models.city import City
from apps.cities.models.metro_line import MetroLine
from apps.cities.models.metro_station import MetroStation


class CreateMetroLinesAndStations:
    lines_file    = Path(settings.BASE_DIR, './classes/generate_content/data/metro/lines.json')
    stations_file = Path(settings.BASE_DIR, './classes/generate_content/data/metro/stations.json')

    count_metro_stations_in_db = MetroStation.objects.all().count()
    count_metro_lines_in_db    = MetroLine.objects.all().count()


    @classmethod
    def create_metro_line(cls, metro_line):
        new_ml = MetroLine()
        new_ml.id = metro_line['id']
        new_ml.name = metro_line['name']
        new_ml.color = metro_line['color']
        new_ml.save()
        print('Metro Line Created!', new_ml.name)


    @classmethod
    def create_metro_station(cls, metro_station: dict):
        get_city       = City.objects.get(id=metro_station['city_id'])
        get_metro_line = MetroLine.objects.get(id=metro_station['line_id'])

        new_ms = MetroStation()
        new_ms.id = metro_station['id']
        new_ms.name = metro_station['name']
        new_ms.metro_line = get_metro_line
        new_ms.city = get_city
        new_ms.save()
        print('Metro Station Created!', new_ms.name)


    @classmethod
    def fill_db(cls):
        if cls.count_metro_lines_in_db == 0:
            for metro_line in read_json_file(cls.lines_file):
                cls.create_metro_line(metro_line)
            else:
                print('Metro Lines already created!')

        if cls.count_metro_stations_in_db == 0:
            for metro_station in read_json_file(cls.stations_file):
                cls.create_metro_station(metro_station)
        else:
            print('Metro Stations already created!')
