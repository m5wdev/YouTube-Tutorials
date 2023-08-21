from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.users.models import CustomUser
from apps.company.models.point import Point
from apps.cities.models.city import City


class CreatePoints:
    filename    = Path(settings.BASE_DIR, './classes/generate_content/data/company_points_with_metro_stations.json')
    count_in_db = Point.objects.all().count()


    @classmethod
    def add_point_to_db(cls, point: dict):
        new_point = Point()
        new_point.id = point['id']
        new_point.active = True
        new_point.name = ''

        if point['phone'] and point['phone'] != 'None':
            new_point.phone  = point['phone']

        if point['office'] and point['phone'] != 'None':
            new_point.office = point['office']

        new_point.address           = point['address']
        new_point.address_with_city = point['address_with_city']

        new_point.work_time = point['work_time_string']

        new_point.latitude  = point['latitude']
        new_point.longitude = point['longitude']

        new_point.moderated = True

        new_point.city   = City.objects.get(id=point['city_id'])
        new_point.author = CustomUser.objects.get(id=1)

        new_point.save()
        print('Point Created!', new_point.address_with_city)

        try:
            if len(point['metro_stations']) > 0:
                new_point.metro.set(point['metro_stations'])
                print('Metro Stations for Point are set!', new_point.address_with_city)
        except Exception as e:
            print(e)


    @classmethod
    def fill_db(cls, limit: int = None):
        # if cls.count_in_db == 0:
        #     for point in read_json_file(cls.filename):
        #         cls.add_point_to_db(point)
        # else:
        #     print('Points already created')

        if limit:
            i = 1
            limit *= 100
            if cls.count_in_db == 0:
                for point in read_json_file(cls.filename):
                    if i <= limit:
                        cls.add_point_to_db(point)
                        i += 1
                    else:
                        break
            else:
                print('Points already created')
        else:
            if cls.count_in_db == 0:
                for point in read_json_file(cls.filename):
                    cls.add_point_to_db(point)
            else:
                print('Points already created')
