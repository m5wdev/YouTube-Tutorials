from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.company.models.often_repair import OftenRepair
from apps.company.models.company import Company


class AddOftenRepair:
    company_often_repair_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_often_repair.json')
    company_often_repair_items_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_often_repair_items.json')

    count_often_repair = OftenRepair.objects.all().count()


    @classmethod
    def create_often_repair(cls):
        if cls.count_often_repair == 0:
            for item in read_json_file(cls.company_often_repair_items_file):
                new_often_repair = OftenRepair()
                new_often_repair.name = item['often_name']
                new_often_repair.slug = item['slug']
                new_often_repair.save()
                print(f'OftenRepair {new_often_repair.name} created!')
        else:
            print('OftenRepair already in DB')


    @classmethod
    def update_companies_often_repair(cls):
        for item in read_json_file(cls.company_often_repair_file):
            try:
                get_company = Company.objects.get(slug=item['company_slug'])

                often_repair_list = []
                for oft_repair in item['often_repair']:
                    often_repair = OftenRepair.objects.get(slug=oft_repair['slug'])
                    often_repair_list.append(often_repair.id)

                get_company.save()
                get_company.often_repair.set(often_repair_list)
                print(f'OftenRepair added to {get_company.name}')
            except Exception as e:
                print('OftenRepair', e)


    @classmethod
    def fill_db(cls):
        # Add Often repair
        cls.create_often_repair()

        # Update Often repair
        cls.update_companies_often_repair()
