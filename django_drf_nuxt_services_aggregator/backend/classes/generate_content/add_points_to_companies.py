from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.company.models.company import Company
from apps.company.models.point import Point


class AddPointsToCompanies:
    filename = Path(settings.BASE_DIR, './classes/generate_content/data/company_points.json')

    count_companies_in_db = Company.objects.all().count()
    count_points_in_db    = Point.objects.all().count()


    @classmethod
    def update_company_in_db(cls, company_id: int, points_ids: list):
        try:
            company = Company.objects.get(id=company_id)
            company.save()
            company.points.set(points_ids)
            print(f'Company {company.name}, updated Points!')
        except Exception as e:
            print(f'Company ID {company_id}', e)


    @classmethod
    def upd_db(cls):
        for point in read_json_file(cls.filename):
            if len(point['point_id']) > 0:
                cls.update_company_in_db(point['company_id'], point['point_id'])
