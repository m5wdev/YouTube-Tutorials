import uuid, random

from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.company.models.company import Company
from apps.company.models.company_image import CompanyImage
from apps.users.models import CustomUser
from apps.cities.models.city import City
from apps.services.models import Service, CategoryService


class CreateCompanies:
    companies_file            = Path(settings.BASE_DIR, './classes/generate_content/data/companies.json')
    companies_brands_file     = Path(settings.BASE_DIR, './classes/generate_content/data/company_brands_with_ids.json')
    companies_categories_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_categories_with_ids.json')
    company_services_categories_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_services_categories.json')

    count_companies_in_db = Company.objects.all().count()
    count_cat_services    = CategoryService.objects.all().count()


    @classmethod
    def delete_empty_services(cls):
        for service in Service.objects.filter(name=''):
            srv = Service.objects.get(id=service.id)
            srv.delete()
            print(f'Service {srv.id} is Empty and Delete')


    @classmethod
    def create_company_services_categories(cls):
        if cls.count_cat_services == 0:
            for item in read_json_file(cls.company_services_categories_file):
                # Top level caegories
                if item['slug'] == 'NULL' and item['parent'] == 'NULL':
                    new_category_service = CategoryService()
                    new_category_service.id = item['id']
                    new_category_service.name = item['name']
                    new_category_service.save()
                    print(f'CategoryService {new_category_service.name} created!')

                # Categories with parents
                if item['slug'] == 'NULL' and item['parent'] != 'NULL':
                    new_category_service = CategoryService()
                    new_category_service.id = item['id']
                    new_category_service.name = item['name']
                    new_category_service.parent_category = CategoryService.objects.get(id=item['parent'])
                    new_category_service.save()
                    print(f'CategoryService {new_category_service.name} with parent {new_category_service.parent_category} created!')

            # services
            for item in read_json_file(cls.company_services_categories_file):
                if item['slug'] != 'NULL' and item['parent'] != 'NULL':
                    new_service = Service()
                    new_service.id     = item['id']
                    new_service.name   = item['name']
                    new_service.slug   = item['slug']
                    new_service.category = CategoryService.objects.get(id=item['parent'])
                    new_service.save()
                    print(f'Service {new_service.name} created!')

            # delete empty services
            cls.delete_empty_services()
        else:
            print(f'CategoryService and Service already created!')


    @classmethod
    def create_company(cls, company):
        new_company = Company()
        new_company.id = company['id']
        new_company.active = True
        new_company.name = company['name']

        try:
            new_company.slug = company['slug']
        except Exception as e:
            new_company.slug = str(uuid.uuid4())

        new_company.body = company['description']

        if company['email'] and company['email'] != 'None':
            new_company.email = str(company['email']).lower()

        if company['url'] and company['url'] != 'None':
            new_company.url   = str(company['url']).lower()

        new_company.phone = company['phone']

        # logo = ProcessedImageField(verbose_name='Логотип компании',
        #                             upload_to=company_logo_upload,
        #                             # processors=[ResizeToFill(512, 512)],
        #                             processors=[ResizeToFit(512, 512)],
        #                             format='JPEG',
        #                             options={'quality': 75},
        #                             blank=True, null=True)

        new_company.courier_departure = company['courier_departure']
        new_company.master_departure = company['master_departure']
        new_company.free_diagnostics = company['no_cost_diagnostics']
        new_company.quick_repair = company['fast_repair']
        new_company.pay_after_repair = company['pay_after_repair']
        new_company.own_warehouse = company['own_warehouse']
        new_company.free_parking = company['free_parking']
        new_company.fix_price = company['fix_price']
        new_company.cash_pay = company['cash_pay']
        new_company.card_pay = company['card_pay']
        new_company.owner_register = company['owner_register']

        if company['min_price'] != 0:
            new_company.min_price = company['min_price']
        if company['min_price'] != 0:
            new_company.max_price = company['max_price']

        # try:
        #     if company['number_of_employees'] != 1:
        #         new_company.number_of_employees = int(company['number_of_employees'])
        # except Exception as e:
        #     pass

        # try:
        #     new_company.year_of_foundation = company['year_of_foundation']
        # except Exception as e:
        #     pass

        if company['ya_id'] != 0:
            new_company.ya_id = company['ya_id']

        new_company.ya_categories = company['ya_categories']
        new_company.ya_services = company['ya_services']

        new_company.city = City.objects.get(id=company['city_id'])
        new_company.author = CustomUser.objects.get(id=1)

        new_company.save()
        print('Company Created!', new_company.name)

        # Add Brands to Company
        for item in read_json_file(cls.companies_brands_file):
            if new_company.id == item['company_id']:
                new_company.brands.set(item['brands_id'])
                print(f'Brands for Company {new_company.name} are set!')

        # Add Categories to Company
        for item in read_json_file(cls.companies_categories_file):
            if new_company.id == item['company_id']:
                new_company.categories.set(item['tech_id'])
                print(f'Categories for Company {new_company.name} are set!')

        # Add FAKE CompanyImages
        # for _ in range(random.randint(0, 9)):
        #     new_company_img = CompanyImage()
        #     new_company_img.company = Company.objects.get(id=new_company.id)
        #     new_company_img.image = 'no-image.jpg'
        #     new_company_img.save()
        #     print(f'Company Image for {new_company.name} added!')


    @classmethod
    def fill_db(cls, limit: int = None):
        # limit = int(limit)

        # Create Services Categories
        cls.create_company_services_categories()

        if limit:
            i = 1
            # if cls.count_companies_in_db == 0:
            for company in read_json_file(cls.companies_file):
                if i <= limit:
                    cls.create_company(company)
                    i += 1
                else:
                    break
            else:
                print('Companies already created!')
        else:
            # if cls.count_companies_in_db == 0:
            for company in read_json_file(cls.companies_file):
                cls.create_company(company)
            else:
                print('Companies already created!')
