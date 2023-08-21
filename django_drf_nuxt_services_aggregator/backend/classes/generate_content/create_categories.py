from .methods import read_json_file
import random
from pathlib import Path
from django.conf import settings
from apps.company.models.category import Category


important = [True, False]

class CreateCategories:
    categories_top_file        = Path(settings.BASE_DIR, './classes/generate_content/data/categories/categories_top.json')
    company_tech_with_ids_file = Path(settings.BASE_DIR, './classes/generate_content/data/categories/company_tech_with_ids.json')
    count_in_db = Category.objects.all().count()


    @classmethod
    def create_category_top(cls, category: list):
        new_cat = Category()
        new_cat.name      = category[1]
        new_cat.slug      = category[2]
        new_cat.important = random.choice(important)
        new_cat.save()
        print('Category created!', new_cat.name)


    @classmethod
    def create_category_child(cls, category: dict):
        new_cat = Category()
        new_cat.id               = category['id']
        new_cat.name             = category['name']
        new_cat.slug             = category['slug']
        new_cat.declension_one_p = category['declension_one_p']
        new_cat.parent_category  = Category.objects.get(id=category['category_id'])
        new_cat.save()
        print('Category created!', new_cat.name)


    @classmethod
    def fill_db(cls):
        if cls.count_in_db == 0:
            for cat in read_json_file(cls.categories_top_file):
                cls.create_category_top(cat)

            for cat in read_json_file(cls.company_tech_with_ids_file):
                cls.create_category_child(cat)
        else:
            print('Categories already created')
