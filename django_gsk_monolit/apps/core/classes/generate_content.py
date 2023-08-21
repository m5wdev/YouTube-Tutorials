import datetime, random
from django.utils import timezone

from django.db.models import Count
from faker import Faker

from django.utils.text import slugify
from transliterate import translit

from apps.realty.models.object import Object
from apps.realty.models.object_video import ObjectVideo
from apps.realty.models.object_file import ObjectFile
from apps.realty.models.object_document import ObjectDocumentAuthor, ObjectDocument
from apps.realty.models.object_info_tab import ObjectInfoTab
from apps.realty.models.object_block import ObjectBlock
from apps.realty.models.object_section import ObjectSection
from apps.realty.models.object_elevator import ObjectElevator
from apps.realty.models.object_gallery import ObjectGallery, ObjectGalleryImage
from apps.realty.models.object_building_types import ObjectBuildingTypes
from apps.realty.models.object_types import ObjectTypes
from apps.realty.models.object_cities import ObjectCities

from apps.realty.models.object_site import ObjectSite, ObjectSiteWindowsView
from apps.realty.models.object_site_balcony import ObjectBalcony
from apps.realty.models.object_site_bathroom import ObjectBathroom

from apps.realty.models.object_commercial import ObjectCommercial
from apps.realty.models.object_commercial_site import ObjectCommercialSite
from apps.realty.models.object_commercial_info_tab import ObjectCommercialInfoTab

from apps.mortgage.models import WayToBuy, Bank, Offer

from apps.news.models.news import NewsCategory, News, NewsImage
from apps.news.models.actions import Actions, ActionsPartner

from apps.company.models.certificate import Certificate
from apps.company.models.management import Management
from apps.company.models.responsibility import Responsibility
from apps.company.models.job import JobBlock, JobVacancy
from apps.company.models.history import History
from apps.company.models.structure import Structure
from apps.company.models.partner import Partner
from apps.company.models.tender import Tender, TenderFile, TenderFaq
from apps.company.models.contacts import ContactsGroup, ContactsItem


class GenerateContent:
    def __init__(self):
        self.fake = Faker()
        self.DUMMY_IMG = 'dummy-image.jpg'
        self.DUMMY_DOCUMENT = 'dummy-document.pdf'

    def get_random_list_item(self, list):
        return random.choice(list)

    def _get_objects_ids_list(self, object_name) -> list:
        return list(object_name.objects.order_by('id').values_list('id', flat=True))

    def _get_tenders_ids_list(self) -> list:
        return list(Tender.objects.order_by('id').values_list('id', flat=True))

    def convert_tuple_to_flat_list(self, tuple):
        return [x[0] for x in tuple]

    def countModelObjects(self, model_name):
        return model_name.objects.all().count()

    def countSitesInObject(self, object_id) -> int:
        return ObjectSite.objects.annotate(Count('object')).filter(object=object_id).count()

    def countCommercialSitesInObjectCommercial(self, object_commercial_id) -> int:
        return ObjectCommercialSite.objects.annotate(Count('object_commercial')).filter(object_commercial=object_commercial_id).count()


    """ [Company] """
    def _create_Certificate(self):
        title = f'Сертификат {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()}'

        certificate = Certificate(title=title, image=self.DUMMY_IMG)
        certificate.save()
        print(f'[Certificate] {certificate.title} created')


    def _create_Management(self):
        position = f'Должность {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()}'

        management = Management(image=self.DUMMY_IMG, surname='Фамилия', name='Имя', patronymic='Отчество', position=position)
        management.save()
        print(f'[Management] {management.position} created')


    def _create_Responsibility(self):
        title = f'Ответственность {self.fake.word()} {self.fake.word()} {self.fake.word()}'

        responsibility = Responsibility(title=title, body=self.fake.text(600), image=self.DUMMY_IMG)
        responsibility.save()
        print(f'[Responsibility] {responsibility.title} created')


    def _create_JobBlock(self):
        title = f'Блок работа {self.fake.word()} {self.fake.word()} {self.fake.word()}'

        job_block = JobBlock(title=title, body=self.fake.text(600), image=self.DUMMY_IMG)
        job_block.save()
        print(f'[JobBlock] {job_block.title} created')


    def _create_JobVacancy(self):
        title = f'Вакансия {self.fake.word()} {self.fake.word()} {self.fake.word()}'

        job_vacancy = JobVacancy(title=title, \
                                 experience='3 - 6 лет', \
                                 duties=self.fake.text(600), \
                                 requirements=self.fake.text(500), \
                                 terms=self.fake.text(300), \
                                 salary='от 30 000 руб./мес', \
                                 contacts='<p><em>Телефон: <a href=\"tel:+79788164888\">+7 (978) 816-48-88</a> (Ольга)<br>\
                                            Почта: <a href=\"mailto:personal@monolit.net\">personal@monolit.net</a></em></p>'
                                )
        job_vacancy.save()
        print(f'[JobVacancy] {job_vacancy.title} created')


    def _create_History(self):
        years_range = [r for r in range(2005, datetime.date.today().year + 1)]

        for year in years_range:
            history = History(year=year, body=self.fake.text(600), image=self.DUMMY_IMG)
            history.save()
            print(f'[History] {history.year} created')


    def _create_Structure(self):
        structure = Structure(url='http://monolit.site', body=self.fake.text(500), image=self.DUMMY_IMG)
        structure.save()
        print(f'[Structure] created')


    def _create_Partner(self):
        partner = Partner(url='https://google.com', image=self.DUMMY_IMG)
        partner.save()
        print(f'[Partner] created')


    def _create_Tender(self):
        title = f'Тендер {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()}'.title()
        tender_cregories_list = self.convert_tuple_to_flat_list(Tender.CATEGORIES)

        tender = Tender(active=self.fake.boolean(chance_of_getting_true=85), \
                        title=title, \
                        category=self.fake.word(tender_cregories_list), \
                        duties=self.fake.text(600), \
                        requirements=self.fake.text(500), \
                        contacts='<p><em>Телефон: <a href=\"tel:+79788164888\">+7 (978) 816-48-88</a> (Ольга)<br>\
                                   Почта: <a href=\"mailto:personal@monolit.net\">personal@monolit.net</a></em></p>'
                        )
        tender.save()
        print(f'[Tender] {tender.title} created')


    def _create_TenderFile(self, tender_id):
        count_files_rel_to_tender = TenderFile.objects.annotate(Count('tender')).filter(tender=tender_id).count()

        if count_files_rel_to_tender < 10:
            tender = Tender.objects.get(pk=tender_id)
            tender_file = TenderFile(tender=tender, name='Документ с описанием тенедера', file=self.DUMMY_DOCUMENT)
            tender_file.save()
            print(f'[TenderFile] for Tender {tender_file.tender} created')


    def _create_TenderFaq(self):
        question = f'Вопрос {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()}'.title()
        tender_faq = TenderFaq(question=question, answer=self.fake.text(600))
        tender_faq.save()
        print(f'[TenderFaq] {tender_faq.question} created')


    def _create_ContactsItem(self, сontacts_group_id):
        сontact_type_list = self.convert_tuple_to_flat_list(ContactsItem.CONTACTS_TYPES)
        сontacts_group = ContactsGroup.objects.get(pk=сontacts_group_id)

        сontact_type = self.fake.word(сontact_type_list)
        contact = 'Something went wrong =('
        if сontact_type == 'email':
            contact = 'mail@monolit.net'
        elif сontact_type == 'phone':
            contact = '+79270004411'

        сontacts_item = ContactsItem(сontacts_group=сontacts_group, \
                                     сontact_type=сontact_type, \
                                     contact_description='Описание контакта', \
                                     contact=contact)
        сontacts_item.save()
        print(f'[ContactsItem] for {сontacts_item.сontacts_group} created')


    def _create_ContactsGroup(self):
        name = f'Контакт {self.fake.word()} {self.fake.word()} {str(self.fake.random_number(4, True))}'.title()

        сontacts_group = ContactsGroup(name=name, \
                                       address='295034 Республика Крым,<br>г. Симферополь, пр. Победы, 28А<br>(3 этаж), оф. 315, 317', \
                                       work_hours='Пн-Пт c 09:00 до 19:00<br>Сб c 10:00 до 15:00<br>Вс - выходной'
                                      )
        сontacts_group.save()
        print(f'[ContactsGroup] {сontacts_group.name} created')

        for _ in range(4):
            self._create_ContactsItem(сontacts_group.id)


    """ [News] """
    def _create_NewsCategory(self):
        if NewsCategory.objects.all().count() == 0:
            news_cats_list = ['Политика', 'Экономика', 'Строительство']

            for category in news_cats_list:
                news_category = NewsCategory(name=category)
                news_category.save()
                print(f'[NewsCategory] created {news_category.name}')


    def _create_NewsImage(self, news_id):
        count_images_rel_to_news = NewsImage.objects.annotate(Count('news')).filter(news=news_id).count()
        news = News.objects.get(pk=news_id)

        if count_images_rel_to_news == 0:
            for _ in range(10):
                news_image = NewsImage(news=news, image=self.DUMMY_IMG)
                news_image.save()
                print(f'[NewsImage] created for {news_id}')


    def _create_News(self):
        title = f'Новость {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()} {str(self.fake.random_number(3, True))}'.title()

        news = News(title=title, main_image=self.DUMMY_IMG, body=self.fake.text(5000))
        news.save()
        print(f'[News] created {news.title}')

        news.object.set([ self.get_random_list_item(self._get_objects_ids_list(Object)) ])
        news_categories_list = list(NewsCategory.objects.values_list('id', flat=True))
        news.category.set([ self.get_random_list_item(news_categories_list) ])

        self._create_NewsImage(news.id)


    """ [Actions] """
    def _create_ActionsPartner(self, action_id):
        action_id = Actions.objects.get(pk=action_id)
        action_partner = ActionsPartner(action=action_id, \
                                        name='Название компании партнера',
                                        logo=self.DUMMY_IMG,
                                        site_url='https://google.com')
        action_partner.save()
        print(f'[ActionsPartner] created {action_partner.name}')


    def _create_Actions(self):
        title = f'Акция {self.fake.word()} {self.fake.word()} {self.fake.word()} {self.fake.word()} {str(self.fake.random_number(3, True))}'.title()
        action = Actions(active=True, \
                            title=title, \
                            date_start=timezone.now(), \
                            date_end=timezone.now() + timezone.timedelta(days=45), \
                            description=self.fake.text(5000), \
                            partners_title='Заголовок для блока с партнерами акции', \
                            image_card=self.DUMMY_IMG, \
                            image_detail=self.DUMMY_IMG, \
                        )
        action.save()
        print(f'[Actions] created {action.title}')

        for _ in range(8):
            self._create_ActionsPartner(action.id)


    """ [ObjectCommercialSite] """
    def _create_ObjectCommercialSite(self, object_commercial_id):
        site_types_list = self.convert_tuple_to_flat_list(ObjectCommercialSite.SITE_TYPES)

        floors_list = list(range(1, 23))
        site_numbers_list = list(range(1, 200))
        price_per_square_list = list(range(32000, 79000))
        site_area_list = list(range(57, 119))

        sections_rel_to_object_ids_list = list(ObjectSection.objects.filter(object_commercial=object_commercial_id).values_list('id', flat=True))

        sites_qty_list = [15, 105, 39]
        qty = self.get_random_list_item(sites_qty_list)

        if self.countCommercialSitesInObjectCommercial(object_commercial_id) < qty:
            for _ in range(qty - self.countCommercialSitesInObjectCommercial(object_commercial_id)):
                object_section = ObjectSection.objects.get(pk=self.get_random_list_item(sections_rel_to_object_ids_list))
                site_area = self.get_random_list_item(site_area_list)
                object_commercial_site = ObjectCommercialSite(special_offer=self.fake.boolean(chance_of_getting_true=20), \
                                                                object_commercial=ObjectCommercial.objects.get(pk=object_commercial_id), \
                                                                site_type=self.get_random_list_item(site_types_list), \
                                                                object_section=object_section, \
                                                                crm_id=self.fake.random_number(9, True), \
                                                                price_per_square=self.get_random_list_item(price_per_square_list), \
                                                                site_area=site_area, \
                                                                floor=self.get_random_list_item(floors_list), \
                                                                site_number=self.get_random_list_item(site_numbers_list), \
                                                                ceiling_height=2.7, \
                                                                street_entrance=self.fake.boolean(chance_of_getting_true=40), \
                                                                image_planning=self.DUMMY_IMG, \
                                                                image_floor=self.DUMMY_IMG, \
                                                                image_section=self.DUMMY_IMG, \
                                                                image_section_in_object=self.DUMMY_IMG, \
                                                                image_genplan=self.DUMMY_IMG, \
                                                            )
                object_commercial_site.save()
                print(f'[ObjectCommercialSite] {object_commercial_site.crm_id} created for ObjectCommercial {object_commercial_site.object_commercial}')

                # Add Batrooms
                self._create_ObjectBathroom_for_ObjectCommercialSite(object_commercial_site.id)


    def _create_ObjectBathroom(self, object_site_id):
        object_bathroom_list = self.convert_tuple_to_flat_list(ObjectBathroom.BATHROOM_TYPES)
        count_bathrooms_rel_to_object_site = ObjectBathroom.objects.annotate(Count('object_site')).filter(object_site=object_site_id).count()
        object_site = ObjectSite.objects.get(pk=object_site_id)

        if count_bathrooms_rel_to_object_site == 0 or count_bathrooms_rel_to_object_site < 2:
            object_bathroom = ObjectBathroom(object_site=object_site, bathroom_type=self.get_random_list_item(object_bathroom_list))
            object_bathroom.save()
            print(f'[ObjectBathroom] created for ObjectSite {object_site}')


    def _create_ObjectBathroom_for_ObjectCommercialSite(self, object_site_id):
        object_bathroom_list = self.convert_tuple_to_flat_list(ObjectBathroom.BATHROOM_TYPES)
        count_bathrooms_rel_to_object_site = ObjectBathroom.objects.annotate(Count('object_commercial_site')).filter(object_commercial_site=object_site_id).count()
        object_commercial_site = ObjectCommercialSite.objects.get(pk=object_site_id)

        if count_bathrooms_rel_to_object_site == 0 or count_bathrooms_rel_to_object_site < 2:
            object_bathroom = ObjectBathroom(object_commercial_site=object_commercial_site, bathroom_type=2)
            object_bathroom.save()
            print(f'[ObjectBathroom] created for ObjectCommercialSite {object_commercial_site}')


    def _create_ObjectBalcony(self, object_site_id):
        object_balcony_list = self.convert_tuple_to_flat_list(ObjectBalcony.BALCONY_TYPES)
        count_balconies_rel_to_object_site = ObjectBalcony.objects.annotate(Count('object_site')).filter(object_site=object_site_id).count()
        object_site = ObjectSite.objects.get(pk=object_site_id)

        if count_balconies_rel_to_object_site == 0 or count_balconies_rel_to_object_site < 2:
            object_balcony = ObjectBalcony(object_site=object_site, balcony_type=self.get_random_list_item(object_balcony_list))
            object_balcony.save()
            print(f'[ObjectBalcony] created for ObjectSite {object_site}')


    def _create_ObjectSite(self, object_id):
        site_types_list = self.convert_tuple_to_flat_list(ObjectSite.SITE_TYPES)

        rooms_qty_list = self.convert_tuple_to_flat_list(ObjectSite.ROOMS_QTY)
        finishing_types_list = self.convert_tuple_to_flat_list(ObjectSite.FINISHING_TYPES)

        object = Object.objects.get(pk=object_id)

        floors_list = list(range(1, 23))
        site_numbers_list = list(range(100, 200))
        price_per_square_list = list(range(52125, 89680))
        site_area_list = list(range(34, 119))
        kitchen_area_list = list(range(10, 15))

        sections_rel_to_object_ids_list = list(ObjectSection.objects.filter(object=object).values_list('id', flat=True))

        # sites_qty_list = list(range(51, 126))
        sites_qty_list = [15, 105, 51, 116, 39]
        qty = self.get_random_list_item(sites_qty_list)

        if self.countSitesInObject(object_id) < qty:
            for _ in range(qty - self.countSitesInObject(object_id)):
                site_area = self.get_random_list_item(site_area_list)
                calc_living_area = site_area - 15.26

                object_section = ObjectSection.objects.get(pk=self.get_random_list_item(sections_rel_to_object_ids_list))

                object_site = ObjectSite(special_offer=self.fake.boolean(chance_of_getting_true=20), \
                                            object=object, \
                                            site_type=self.get_random_list_item(site_types_list), \
                                            object_section=object_section, \
                                            crm_id=self.fake.random_number(9, True), \
                                            floor=self.get_random_list_item(floors_list), \
                                            site_number=self.get_random_list_item(site_numbers_list), \
                                            price_per_square=self.get_random_list_item(price_per_square_list), \
                                            rooms_qty=self.get_random_list_item(rooms_qty_list), \
                                            site_area=site_area, \
                                            living_area=calc_living_area, \
                                            kitchen_area=self.get_random_list_item(kitchen_area_list), \
                                            ceiling_height=2.7,\
                                            two_levels=self.fake.boolean(chance_of_getting_true=20), \
                                            entresol=self.fake.boolean(chance_of_getting_true=30), \
                                            wardrobe=self.fake.boolean(chance_of_getting_true=40), \
                                            finish_type=self.get_random_list_item(finishing_types_list), \
                                            image_planning=self.DUMMY_IMG, \
                                            image_planning3d=self.DUMMY_IMG, \
                                            image_floor=self.DUMMY_IMG, \
                                            image_section=self.DUMMY_IMG, \
                                            image_section_in_object=self.DUMMY_IMG, \
                                            image_genplan=self.DUMMY_IMG, \
                                        )
                object_site.save()

                # Set ObjectSiteWindowsView
                windows_view_list = list(ObjectSiteWindowsView.objects.values_list('id', flat=True))
                object_site.window_view.set([self.get_random_list_item(windows_view_list), self.get_random_list_item(windows_view_list)])

                print(f'[ObjectSite] {object_site.crm_id} created for Object {object_id}')

            # Add Balconies
            for _ in range(2):
                self._create_ObjectBalcony(object_site.id)

            # Add Batrooms
            for _ in range(2):
                self._create_ObjectBathroom(object_site.id)

        print(f'\nВ Объекте {object_id}, {self.countSitesInObject(object_id)} квартир, было создано, {qty} квартир')


    """ [Mortgage] """
    def _create_Offer(self):
        banks_ids = list(Bank.objects.order_by('id').values_list('id', flat=True))
        bank = Bank.objects.get(pk=self.get_random_list_item(banks_ids))

        first_payment_from_list = [15, 20]
        first_payment_to_list = [15, 20]

        loan_term_from_list = [1, 3]
        loan_term_to_list = [25, 30]

        rate_from_list = [11.7, 11]
        rate_to_list = [11.7, 12]

        offer = Offer(bank=bank,\
                      title=f'Ипотечная программа {str(self.fake.word()).title()} {str(self.fake.random_number(4, True))}', \
                      first_payment_from=self.get_random_list_item(first_payment_from_list), \
                      first_payment_to=self.get_random_list_item(first_payment_to_list), \
                      loan_term_from=self.get_random_list_item(loan_term_from_list), \
                      loan_term_to=self.get_random_list_item(loan_term_to_list), \
                      rate_from=self.get_random_list_item(rate_from_list), \
                      rate_to=self.get_random_list_item(rate_to_list), \
                      description=self.fake.text(500)
                    )
        offer.save()

        # Apply Offer to an Objects
        objects_ids_list = list(self._get_objects_ids_list(Object))
        offer.object.set(objects_ids_list)
        print(f'[Offer] {offer.title} created')


    def _create_Bank(self):
        if Bank.objects.all().count() > 0:
            print('[Bank] already created')
        else:
            bank = Bank(name='РНКБ', logo=self.DUMMY_IMG)
            bank.save()

            bank = Bank(name='Банк Россия', logo=self.DUMMY_IMG)
            bank.save()
            print('[Bank] are created')


    def _create_WayToBuy(self):
        objects_ids = self._get_objects_ids_list(Object)
        way_to_buy = WayToBuy()

        if WayToBuy.objects.filter(pk=1).count() == 0:
            way_to_buy.save()
            way_to_buy.military.set(objects_ids)
            way_to_buy.mother.set(objects_ids)
            print(f'[WayToBuy] is created')
        else:
            way_to_buy = WayToBuy.objects.get(pk=1)
            way_to_buy.save()
            way_to_buy.military.set(objects_ids)
            way_to_buy.mother.set(objects_ids)
            print(f'[WayToBuy] is updated')


    """ [Object] """
    def _create_ObjectGalleryImage(self, gallery_id, qty: int):
        count_images_in_gallery = ObjectGalleryImage.objects.annotate(Count('gallery')).filter(gallery=gallery_id).count()

        if count_images_in_gallery == 0:
            gallery = ObjectGallery.objects.get(pk=gallery_id)
            for _ in range(qty):
                gallery_image = ObjectGalleryImage(gallery=gallery, image=self.DUMMY_IMG)
                gallery_image.save()
            print(f'[GalleryImage] created for Gallery {gallery_id}')


    def _create_ObjectGallery(self, object_id, gal_names: list):
        count_object_galleries = ObjectGallery.objects.annotate(Count('object')).filter(object=object_id).count()

        if count_object_galleries == 0:
            object = Object.objects.get(pk=object_id)
            for gal_name in gal_names:
                object_gallery = ObjectGallery(object=object, name=gal_name)
                object_gallery.save()
                print(f'[Gallery "{gal_name}"] created for Object {object_id}')
                # Create gallery images
                self._create_ObjectGalleryImage(object_gallery.id, 7)


    def _create_ObjectDocumentAuthor(self):
        author_name = 'Иванов А.П.'
        count_object_document_authors = ObjectDocumentAuthor.objects.annotate(Count('name')).filter(name=author_name).count()

        if count_object_document_authors == 0:
            object_document_author = ObjectDocumentAuthor(name=author_name)
            object_document_author.save()
            print(f'[ObjectDocumentAuthor "{author_name}"] created')


    def _create_ObjectDocument(self, object_id, qty: int):
        count_documents_rel_to_object = ObjectDocument.objects.annotate(Count('object')).filter(object=object_id).count()

        if count_documents_rel_to_object == 0:
            for _ in range(qty):
                document_fake_title = f'Документ {self.fake.word()} {self.fake.word()} {self.fake.random_number(10, True)}'

                object = Object.objects.get(pk=object_id)
                object_document_author = ObjectDocumentAuthor.objects.first()

                object_document = ObjectDocument(object=object, title=document_fake_title, author=object_document_author, file=self.DUMMY_DOCUMENT)
                object_document.save()
                print(f'[ObjectDocument "{document_fake_title}"] created for Object {object_id}')


    def _create_ObjectElevator(self, object_section_id):
        count_elevators_rel_to_section = ObjectElevator.objects.annotate(Count('object_section')).filter(object_section=object_section_id).count()

        if count_elevators_rel_to_section == 0:
            elevator_types_list = self.convert_tuple_to_flat_list(ObjectElevator.ELEVATORS_TYPES)
            object_section = ObjectSection.objects.get(pk=object_section_id)

            object_elevator = ObjectElevator(object_section=object_section, \
                                             elevator_type=elevator_types_list[0], \
                                             elevator_qty=2
                                            )
            object_elevator.save()
            print(f'[ObjectElevator "{elevator_types_list[0]}"] created for ObjectSection {object_section_id}')

            object_elevator = ObjectElevator(object_section=object_section, \
                                             elevator_type=elevator_types_list[1], \
                                             elevator_qty=1
                                            )
            object_elevator.save()
            print(f'[ObjectElevator {elevator_types_list[1]}] created for ObjectSection {object_section_id}')


    def _create_ObjectSection(self, object_id):
        count_sections_rel_to_object = ObjectSection.objects.annotate(Count('object')).filter(object=object_id).count()

        if count_sections_rel_to_object == 0:
            object_blocks_ids = ObjectBlock.objects.filter(object=object_id).values_list('id', flat=True)
            i = 1
            for object_block_id in object_blocks_ids:
                object = Object.objects.get(pk=object_id)
                object_block = ObjectBlock.objects.filter(object=object_id).get(pk=object_block_id)
                object_section = ObjectSection(object=object, \
                                                object_block=object_block, \
                                                name=f'С{i}.{i}', \
                                                comlete_year=self.get_random_list_item([2019, 2020, 2021, 2022]), \
                                                floor_first=1, \
                                                floor_last=23, \
                                            )
                object_section.save()
                print(f'[ObjectSection "{object_section.name}"] created for Object {object_id}')
                i += 1
                # Create Elevators for Section
                self._create_ObjectElevator(object_section.id)

    # Section for ObjectCommercial
    def _create_ObjectSection_for_ObjectCommercial(self, object_commercial_id):
        count_sections_rel_to_object_commercial = ObjectSection.objects.annotate(Count('object_commercial')).filter(object_commercial=object_commercial_id).count()

        if count_sections_rel_to_object_commercial == 0:
            object_commercial_blocks_ids = ObjectBlock.objects.filter(object_commercial=object_commercial_id).values_list('id', flat=True)
            i = 1
            for object_commercial_block_id in object_commercial_blocks_ids:
                object_commercial = ObjectCommercial.objects.get(pk=object_commercial_id)
                object_commercial_block = ObjectBlock.objects.filter(object_commercial=object_commercial_id).get(pk=object_commercial_block_id)
                object_commercial_section = ObjectSection(object_commercial=object_commercial, \
                                                            object_block=object_commercial_block, \
                                                            name=f'С{i}.к{i}', \
                                                            comlete_year=self.get_random_list_item([2019, 2020, 2021, 2022]), \
                                                            floor_first=1, \
                                                            floor_last=23, \
                                                        )
                object_commercial_section.save()
                print(f'[ObjectSection "{object_commercial_section.name}"] created for ObjectCommercial {object_commercial_section.id}')
                i += 1
                # Create Elevators for Section
                self._create_ObjectElevator(object_commercial_section.id)


    def _create_ObjectBlock(self, object_id, qty: int):
        count_blocks_rel_to_object = ObjectBlock.objects.annotate(Count('object')).filter(object=object_id).count()

        if count_blocks_rel_to_object == 0:
            i = 1
            for _ in range(qty):
                object_block = ObjectBlock(object=Object.objects.get(pk=object_id), name=f'Блок {i}')
                object_block.save()
                print(f'[ObjectBlock "{object_block.name}"] created for Object {object_id}')
                i += 1

    # Block for ObjectCommercial
    def _create_ObjectBlock_for_ObjectCommercial(self, object_commercial_id, qty: int):
        count_blocks_rel_to_object_commercial = ObjectBlock.objects.annotate(Count('object_commercial')).filter(object_commercial=object_commercial_id).count()

        if count_blocks_rel_to_object_commercial == 0:
            i = 1
            for _ in range(qty):
                object_commercial_block = ObjectBlock(object_commercial=ObjectCommercial.objects.get(pk=object_commercial_id), name=f'Блок {i}')
                object_commercial_block.save()
                print(f'[ObjectBlock "{object_commercial_block.name}"] created for ObjectCommercial {object_commercial_block.id}')
                i += 1


    def _create_ObjectInfoTab(self, object_id):
        count_info_tabs_rel_to_object = ObjectInfoTab.objects.annotate(Count('object')).filter(object=object_id).count()
        object_info_tab_icons_list = self.convert_tuple_to_flat_list(ObjectInfoTab.ICONS)
        object = Object.objects.get(pk=object_id)

        if count_info_tabs_rel_to_object == 0:
            for info_tab in object_info_tab_icons_list:
                object_info_tab = ObjectInfoTab(object=object, icon_name=info_tab, description=self.fake.text(300), image=self.DUMMY_IMG)
                object_info_tab.save()
                print(f'[ObjectInfoTab "{info_tab}"] created for Object {object_id}')


    def _create_ObjectCommercialInfoTab(self, object_commercial_id):
        count_info_tabs_rel_to_object = ObjectCommercialInfoTab.objects.annotate(Count('object_commercial')).filter(object_commercial=object_commercial_id).count()
        object_info_tab_icons_list = self.convert_tuple_to_flat_list(ObjectCommercialInfoTab.ICONS)
        object_commercial = ObjectCommercial.objects.get(pk=object_commercial_id)

        if count_info_tabs_rel_to_object == 0:
            for info_tab in object_info_tab_icons_list:
                object_info_tab = ObjectCommercialInfoTab(object_commercial=object_commercial, icon_name=info_tab, description=self.fake.text(300), image=self.DUMMY_IMG)
                object_info_tab.save()
                print(f'[ObjectCommercialInfoTab "{info_tab}"] created for ObjectCommercial {object_commercial_id}')


    def _create_ObjectFile(self, object_id):
        count_files_rel_to_object = ObjectFile.objects.annotate(Count('object')).filter(object=object_id).count()

        if count_files_rel_to_object == 0:
            i = 1
            for _ in range(6):
                object = Object.objects.get(pk=object_id)
                object_file = ObjectFile(object=object, name=f'Файл объекта {i}', file=self.DUMMY_DOCUMENT)
                object_file.save()
                print(f'[ObjectFile {object_file.name}] created for Object {object_id}')
                i += 1


    def _create_ObjectVideo(self, object_id, qty: int):
        count_videos_rel_to_object = ObjectVideo.objects.annotate(Count('object')).filter(object=object_id).count()

        if count_videos_rel_to_object == 0:
            for _ in range(qty):
                object = Object.objects.get(pk=object_id)
                object_video = ObjectVideo(object=object, video='https://www.youtube.com/watch?v=F5mRW0jo-U4')
                object_video.save()
                print(f'[ObjectVideo] created for Object {object_id}')


    def _create_Object(self):
        name = f'Объект {self.fake.word()} {str(self.fake.random_number(4, True))}'.title()
        city = ObjectCities.objects.get(name='Симферополь')
        fake = Faker()
        object = Object(completed=self.fake.boolean(chance_of_getting_true=40), \
                        all_sold=self.fake.boolean(chance_of_getting_true=30), \
                        partnership=fake.boolean(chance_of_getting_true=20), \
                        crm_id=self.fake.random_number(7, True), \
                        name=name, \
                        slug=slugify(translit(name, 'ru', reversed=True)), \
                        object_type=ObjectTypes.objects.get(id=5), \
                        building_type=ObjectBuildingTypes.objects.get(id=1), \
                        description=self.fake.text(1000), \
                        city=city, \
                        address='ул. Ленина 12', \
                        genplan=self.DUMMY_IMG, \
                        main_image=self.DUMMY_IMG, \
                        slider_main_image=self.DUMMY_IMG, \
                        webcam='https://rtsp.me/embed/3KASrTkG/', \
                        panoram='https://monolit360.com/files/main/index.html?s=pano1692', \
                    )
        object.save()
        # Set ManyToMany categories
        # object.category.set([1, 2])
        print(f'[Object] (ID: {object.id}) created "{name}"')


    def _create_ObjectCommercial(self):
        name = f'Коммерческий Объект {self.fake.word()} {str(self.fake.random_number(4, True))}'.title()
        object_commercial = ObjectCommercial(completed=self.fake.boolean(chance_of_getting_true=40), \
                                            all_sold=self.fake.boolean(chance_of_getting_true=30), \
                                            crm_id=self.fake.random_number(7, True), \
                                            name=name, \
                                            slug=slugify(translit(name, 'ru', reversed=True)), \
                                            object_type=ObjectTypes.objects.get(id=1), \
                                            building_type=ObjectBuildingTypes.objects.get(id=1), \
                                            description=self.fake.text(1000), \
                                            city=ObjectCities.objects.get(name='Симферополь'), \
                                            address='пр. Победы, 28А', \
                                            genplan=self.DUMMY_IMG, \
                                            main_image=self.DUMMY_IMG, \
                                            slider_main_image=self.DUMMY_IMG, \
                                            webcam='https://rtsp.me/embed/3KASrTkG/', \
                                            panoram='https://monolit360.com/files/main/index.html?s=pano1692', \
                                        )
        object_commercial.save()
        print(f'[ObjectCommercial] (ID: {object_commercial.id}) created "{name}"')


    def fillEntireSite(self, quantity):
        for _ in range(quantity):
            self._create_Object()
            # self._create_ObjectCommercial()
        print('\n')

        # Fill related to Objects models with content
        for object_id in self._get_objects_ids_list(Object):
            self._create_ObjectVideo(object_id, 4)
            self._create_ObjectFile(object_id)
            self._create_ObjectInfoTab(object_id)
            self._create_ObjectBlock(object_id, 4)
            self._create_ObjectSection(object_id)
            self._create_ObjectGallery(object_id, ['Июль 2019', 'Сентябрь 2019', 'Ноябрь 2019'])

        # Fill Objects with Documents
        self._create_ObjectDocumentAuthor()

        for object_id in self._get_objects_ids_list(Object):
            self._create_ObjectDocument(object_id, 53)

        # Fill Mortgage
        self._create_WayToBuy()

        if self.countModelObjects(Bank) < 3:
            for _ in range(3):
                self._create_Bank()

        self._create_Offer()

        # Generate ObjectSite
        for object_id in self._get_objects_ids_list(Object):
            self._create_ObjectSite(object_id)

        self._create_NewsCategory()
        if self.countModelObjects(News) < 200:
            for _ in range(25):
                self._create_News()

        if self.countModelObjects(Actions) < 18:
            for _ in range(18):
                self._create_Actions()

        if self.countModelObjects(Certificate) < 8:
            for _ in range(8):
                self._create_Certificate()

        if self.countModelObjects(Management) < 6:
            for _ in range(6):
                self._create_Management()

        if self.countModelObjects(Responsibility) < 10:
            for _ in range(10):
                self._create_Responsibility()

        if self.countModelObjects(JobBlock) < 5:
            for _ in range(5):
                self._create_JobBlock()

        if self.countModelObjects(JobVacancy) < 16:
            for _ in range(16):
                self._create_JobVacancy()

        if self.countModelObjects(History) == 0:
            self._create_History()

        if self.countModelObjects(Structure) < 15:
            for _ in range(15):
                self._create_Structure()

        if self.countModelObjects(Partner) < 8:
            for _ in range(8):
                self._create_Partner()

        if self.countModelObjects(Tender) < 25:
            for _ in range(25):
                self._create_Tender()

        for tender_id in self._get_tenders_ids_list():
            for _ in range(random.randrange(10)):
                self._create_TenderFile(tender_id)

        if self.countModelObjects(TenderFaq) < 30:
            for _ in range(30):
                self._create_TenderFaq()

        if self.countModelObjects(ContactsGroup) < 7:
            for _ in range(7):
                self._create_ContactsGroup()

        # ObjectCommercial
        for _ in range(quantity):
            self._create_ObjectCommercial()
        print('\n')

        for object_commercial_id in self._get_objects_ids_list(ObjectCommercial):
            self._create_ObjectBlock_for_ObjectCommercial(object_commercial_id, 4)
            self._create_ObjectSection_for_ObjectCommercial(object_commercial_id)
            self._create_ObjectCommercialInfoTab(object_commercial_id)

        # Generate ObjectCommercialSite
        for object_commercial_id in self._get_objects_ids_list(ObjectCommercial):
            self._create_ObjectCommercialSite(object_commercial_id)
