from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.company.models.company import Company


class AddCompanyLogos:
    company_logos_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_logos.json')


    @classmethod
    def add_company_logos(cls):
        for item in read_json_file(cls.company_logos_file):
            try:
                company = Company.objects.get(slug=item['slug'])
                company.logo = f"{item['logo']}"
                company.save()
                print(f'Company Logo for {company.name} updated!')
            except Exception as e:
                print('AddCompanyLogos', e)

    @classmethod
    def fill_db(cls):
        cls.add_company_logos()
