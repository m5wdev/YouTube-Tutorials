from .methods import read_json_file

from pathlib import Path
from django.conf import settings

from apps.company.models.brand import Brand


class CreateBrands:
    filename                        = Path(settings.BASE_DIR, './classes/generate_content/data/brands.json')
    brands_categories_with_ids_file = Path(settings.BASE_DIR, './classes/generate_content/data/brands_categories_with_ids.json')
    count_in_db = Brand.objects.all().count()


    @classmethod
    def add_brand_to_db(cls, brand: dict):
        new_brand = Brand()
        new_brand.id = brand['id']
        new_brand.name = brand['name']
        new_brand.slug = brand['slug']
        new_brand.save()
        print('Brand Created!', new_brand.name)

        # Add Categories to Brand
        for item in read_json_file(cls.brands_categories_with_ids_file):
            if item['brands_id'] and item['tech_id']:
                if new_brand.id == item['brands_id']:
                    new_brand.categories.set(item['tech_id'])
                    print(f'Categories for Brand {new_brand.name} are set!')


    @classmethod
    def fill_db(cls):
        if cls.count_in_db == 0:
            for brand in read_json_file(cls.filename):
                cls.add_brand_to_db(brand)
        else:
            print('Barands already created')
