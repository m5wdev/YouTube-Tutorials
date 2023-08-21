from .methods import read_json_file
from pathlib import Path
from django.conf import settings

from apps.company.models.company import Company
from apps.company.models.company_image import CompanyImage


class AddCompanyImages:
    company_images_file = Path(settings.BASE_DIR, './classes/generate_content/data/company_images.json')


    @classmethod
    def delete_no_image(cls, company_slug):
        company_images = CompanyImage.objects.filter(company__slug=company_slug)

        for ci in company_images:
            if ci.image == 'no-image.jpg':
                ci.delete()
                print(f'No Image for {company_slug} deleted!')


    @classmethod
    def add_company_images(cls):
        for item in read_json_file(cls.company_images_file):
            cls.delete_no_image(item['company'])

            for img in item['images']:
                try:
                    company_img = CompanyImage()
                    # company_img.company = Company.objects.get_or_create(slug=item['company'], city__slug=item['city'])
                    company_img.company = Company.objects.get(slug=item['company'])
                    company_img.image = f"companies/{item['city']}/{item['company']}/{img}"
                    company_img.save()
                    print(f'Company Image for {company_img.company.name} updated!')
                except Exception as e:
                    print('AddCompanyImages', e)


    @classmethod
    def fill_db(cls):
        cls.add_company_images()
