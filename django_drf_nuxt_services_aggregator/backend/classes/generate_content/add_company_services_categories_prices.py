from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.company.models.company import Company
from apps.services.models import Service

from .create_companies import CreateCompanies


class AddCompanyServicesCategoriesPrices:
    company_services_categories_prices_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_services_categories_prices.json')


    @classmethod
    def company_services_categories_prices(cls):
        for item in read_json_file(cls.company_services_categories_prices_file):
            if len(item['prices']) > 0:
                for price in item['prices']:
                    get_service = Service.objects.get(id=price['service_id'])

                    get_service.price = price['price_from']
                    if price['price_to'] != 0:
                        get_service.price_max = price['price_to']

                    try:
                        get_service.company = Company.objects.get(slug=item['company_slug'])
                        get_service.save()
                        print(f'Service Prices for {get_service.name} in company {get_service.company} are updated!')
                    except Exception as e:
                        print(e)
                        pass

        # delete empty services
        CreateCompanies.delete_empty_services()
