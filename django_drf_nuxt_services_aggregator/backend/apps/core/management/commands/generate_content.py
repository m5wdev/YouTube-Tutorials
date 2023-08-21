from django.core.management.base import BaseCommand
# from django.conf import settings

from classes.generate_content.create_superuser import CreateSuperuser
from classes.generate_content.create_blog_posts import CreateBlogPosts
from classes.generate_content.create_cities import CreateCities
from classes.generate_content.create_metro import CreateMetroLinesAndStations
from classes.generate_content.create_users import CreateUsers
from classes.generate_content.create_brands import CreateBrands
from classes.generate_content.create_categories import CreateCategories
from classes.generate_content.create_companies import CreateCompanies
from classes.generate_content.create_points import CreatePoints
from classes.generate_content.add_points_to_companies import AddPointsToCompanies
from classes.generate_content.add_company_services_categories_prices import AddCompanyServicesCategoriesPrices
from classes.generate_content.company_often_repair import AddOftenRepair
from classes.generate_content.add_company_images import AddCompanyImages
from classes.generate_content.add_company_logos import AddCompanyLogos


class Command(BaseCommand):
    help = 'Fill DB with dummy content'


    def add_arguments(self, parser):
        parser.add_argument(
            '-q',
            '--qty',
            type=int,
            help='Companies quantity to generate',
        )


    def handle(self, *args, **options):
        # if settings.DEBUG:
        # else:
        #     self.stdout.write(self.style.ERROR('Fill Content FAIL (DEBUG = False)'))
        CreateSuperuser.create()
        CreateUsers.fill_db()
        CreateBlogPosts.fill_db()
        CreateCities.fill_db()
        CreateMetroLinesAndStations.fill_db()
        CreateCategories.fill_db()
        CreateBrands.fill_db()

        if options['qty']:
            CreateCompanies.fill_db(options['qty'])
        else:
            CreateCompanies.fill_db()

        if options['qty']:
            CreatePoints.fill_db(options['qty'])
        else:
            CreatePoints.fill_db()

        # NOTE: Update existing info
        AddPointsToCompanies.upd_db()
        AddCompanyServicesCategoriesPrices.company_services_categories_prices()
        AddOftenRepair.fill_db()
        AddCompanyImages.fill_db()
        AddCompanyLogos.fill_db()

        self.stdout.write(self.style.SUCCESS('Fill DB with content: OK'))
