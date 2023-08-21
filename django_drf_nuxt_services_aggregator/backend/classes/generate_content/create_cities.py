from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.cities.models.city import City
from apps.cities.models.subdomain import Subdomain


class CreateCities:
    cities_file = Path(settings.BASE_DIR, './classes/generate_content/data/cities.json')
    count_in_db = City.objects.all().count()


    @classmethod
    def create_subdomain(cls, city: dict):
        new_subdomain = Subdomain()
        new_subdomain.name = city['subdomain']
        new_subdomain.save()
        print('Subdomain Created!', new_subdomain.name)


    @classmethod
    def create_city(cls, city: dict):
        new_city = City()
        new_city.id = city['id']
        new_city.name = city['name']
        new_city.declension_p = city['declension_p']
        new_city.declension_r = city['declension_r']
        new_city.v_declension_p = city['v_declension_p']

        new_city.lower_latitude  = city['lower_latitude']
        new_city.lower_longitude = city['lower_longitude']

        new_city.upper_latitude  = city['upper_latitude']
        new_city.upper_longitude = city['upper_longitude']

        get_subdomain = Subdomain.objects.get(name=city['subdomain'])
        new_city.subdomain = get_subdomain

        new_city.save()
        print('City Created!', new_city.name)


    @classmethod
    def fill_db(cls):
        if cls.count_in_db == 0:
            for city in read_json_file(cls.cities_file):
                cls.create_subdomain(city)
                cls.create_city(city)
        else:
            print('Cities & Subdomains already created!')
