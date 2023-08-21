import random

from django.utils import timezone

from django.contrib.auth.models import Group

from apps.services.models import Services
from apps.account.models import Account
from apps.actions.models import Actions

from apps.salon.models.salon import Salon
from apps.salon.models.salon_services import SalonServices
from apps.salon.models.work_schedule import WorkSchedule
from apps.salon.models.employee import Employee
from apps.salon.models.client_appointment import ClientAppointment
from apps.salon.models.client import Client
from apps.salon.models.address import City, Address, Metro


class AddDummyContent:
    # Create Services from array
    def _createSubServices(self, arr, obj):
        for item in arr:
            try:
                Services.objects.get(name=item)
                print(f'Услуга "{item}" уже существует')
            except Exception as e:
                Services.objects.create(name=item, parent=obj)
                print(f'Услуга "{item}" создана!')


    def addServices(self):
        # Ногтевой сервис
        try:
            nails_root = Services.objects.get(name="Ногтевой сервис")
            print(f'Услуга "{nails_root}" уже существует')
        except Exception as e:
            nails_root = Services.objects.create(name="Ногтевой сервис")
            print(f'Услуга "{nails_root}" создана!')

        # Маникюр
        try:
            manicure_root = Services.objects.get(name="Маникюр", parent=nails_root)
            print(f'Услуга "{manicure_root}" уже существует')
        except Exception as e:
            manicure_root = Services.objects.create(name="Маникюр", parent=nails_root)
            print(f'Услуга "{manicure_root}" создана!')

        # Удаление волос
        # try:
        #     hair_remove_root = Services.objects.get(name="Удаление волос")
        #     print(f'Услуга "{hair_remove_root}" уже существует')
        # except Exception as e:
        #     hair_remove_root = Services.objects.create(name="Удаление волос")
        #     print(f'Услуга "{hair_remove_root}" создана!')

        # Брови и ресницы
        # try:
        #     brows_lashes_root = Services.objects.get(name="Брови и ресницы")
        #     print(f'Услуга "{brows_lashes_root}" уже существует')
        # except Exception as e:
        #     brows_lashes_root = Services.objects.create(name="Брови и ресницы")
        #     print(f'Услуга "{brows_lashes_root}" создана!')

        # Барбершоп
        try:
            barbershop_root = Services.objects.get(name="Барбершоп")
            print(f'Услуга "{barbershop_root}" уже существует')
        except Exception as e:
            barbershop_root = Services.objects.create(name="Барбершоп")
            print(f'Услуга "{barbershop_root}" создана!')


        manicure = [
            'Классический',
            'Европейский',
            'Обрезной',
            'Комбинированный',
            'Аппаратный',
            'Кл. маник+гель лак',
            'Мужской маникюр',
            'Укрепление акрилом',
            'Ремонт ногтя',
            'Выравнивание ногт. Пластины',
            'Наращивание ногтей',
            'Наращивание гелем ногтя',
            'Снятие геля',
            'Снятие гель-лака',
            'Снятие лака',
            'Градиент(1/все)',
            'Френч классический',
            'Френч цветной',
            'Френч обратный',
            'Лунки',
            'Кошачий глаз',
            'Втирка(1/все)',
            'Стразы',
            'Рисунки',
            'Наклейки',
            'Матовое покрытие',
            'Парафинотерапия',
        ]

        self._createSubServices(manicure, manicure_root)

        # Педикюр
        try:
            pedicure_root = Services.objects.get(name="Педикюр", parent=nails_root)
            print(f'Услуга "{pedicure_root}" уже существует')
        except Exception as e:
            pedicure_root = Services.objects.create(name="Педикюр", parent=nails_root)
            print(f'Услуга "{pedicure_root}" создана!')

        pedicure = [
            'Классический',
            'Европейский',
            'Аппаратный',
            'Покрытие гель-лак',
            'Покрытие лак',
            'Кл.пед+гель лак',
            'Удаление натоптышей',
            'Ремонт ногтя',
            'Наращивание гелем',
            'Снятие гель-лака',
            'Мужской педикюр',
        ]

        self._createSubServices(pedicure, pedicure_root)

        # Сеты
        try:
            sets_root = Services.objects.get(name="Сеты", parent=nails_root)
            print(f'Услуга "{sets_root}" уже существует')
        except Exception as e:
            sets_root = Services.objects.create(name="Сеты", parent=nails_root)
            print(f'Услуга "{sets_root}" создана!')

        sets = [
            'Классический маникюр + классический педикюр + гель лак',
            'Классический маникюр + гель лак',
            'Классический педикюр + гель лак',
        ]

        self._createSubServices(sets, sets_root)

        # Парикмахерский зал
        try:
            barber_root = Services.objects.get(name="Парикмахерский зал")
            print(f'Услуга "{barber_root}" уже существует')
        except Exception as e:
            barber_root = Services.objects.create(name="Парикмахерский зал")
            print(f'Услуга "{barber_root}" создана!')

        # Стрижка
        try:
            haircut_root = Services.objects.get(name="Стрижка", parent=barber_root)
            print(f'Услуга "{haircut_root}" уже существует')
        except Exception as e:
            haircut_root = Services.objects.create(name="Стрижка", parent=barber_root)
            print(f'Услуга "{haircut_root}" создана!')

        haircut = [
            'Умная стрижка',
            'Стрижка жгутиками',
            'Подравнивание кончиков',
            'Челка',
            'Мужская стрижка',
        ]

        self._createSubServices(haircut, haircut_root)

        # Окрашивание
        try:
            haircoloring_root = Services.objects.get(name="Окрашивание", parent=barber_root)
            print(f'Услуга "{haircoloring_root}" уже существует')
        except Exception as e:
            haircoloring_root = Services.objects.create(name="Окрашивание", parent=barber_root)
            print(f'Услуга "{haircoloring_root}" создана!')

        haircoloring = [
            'Однотонное',
            'Тонирование',
            'Мелирование',
            'Сложное',
            'Черепаховое',
            'AirTouch',
            'Шатуш',
            'Балаяж',
        ]

        self._createSubServices(haircoloring, haircoloring_root)

        # Укладка
        try:
            hairstyling_root = Services.objects.get(name="Укладка", parent=barber_root)
            print(f'Услуга "{hairstyling_root}" уже существует')
        except Exception as e:
            hairstyling_root = Services.objects.create(name="Укладка", parent=barber_root)
            print(f'Услуга "{hairstyling_root}" создана!')

        hairstyling = [
            'Повседневная укладка',
            'Выпрямление',
            'Голливудские локоны',
            'Локоны на Брашенг',
            'Локоны на Плойку',
            'Вечерняя укладка',
            'Свадебная укладка',
        ]

        self._createSubServices(hairstyling, hairstyling_root)

        # Удаление волос
        try:
            # hairremoving_root = Services.objects.get(name="Удаление волос", parent=barber_root)
            hairremoving_root = Services.objects.get(name="Удаление волос")
            print(f'Услуга "{hairremoving_root}" уже существует')
        except Exception as e:
            # hairremoving_root = Services.objects.create(name="Удаление волос", parent=barber_root)
            hairremoving_root = Services.objects.create(name="Удаление волос")
            print(f'Услуга "{hairremoving_root}" создана!')

        hairremoving = [
            'Глубокое бикини',
            'Классическое бикини',
            'Подмышки',
            'Ноги до колен',
            'Ноги полностью',
            'Руки до локтя',
            'Руки полностью',
            'Усики',
            'Линия живота',
            'Лицо',
        ]

        self._createSubServices(hairremoving, hairremoving_root)

        # Брови и ресницы
        try:
            # eyelashes_eyebrows_root = Services.objects.get(name="Брови и ресницы", parent=barber_root)
            eyelashes_eyebrows_root = Services.objects.get(name="Брови и ресницы")
            print(f'Услуга "{eyelashes_eyebrows_root}" уже существует')
        except Exception as e:
            # eyelashes_eyebrows_root = Services.objects.create(name="Брови и ресницы", parent=barber_root)
            eyelashes_eyebrows_root = Services.objects.create(name="Брови и ресницы")
            print(f'Услуга "{eyelashes_eyebrows_root}" создана!')

        eyelashes_eyebrows = [
            'Лучики',
            'Цветные ресницы',
            'Снятие ресниц',
            'Ламинирование ресниц',
            'Ламинирование бровей',
            'Коррекция бровей',
            'Окрашивание бровей',
            'Окрашивание ресниц',
            'Окрашивание и коррекция бровей',
        ]

        self._createSubServices(eyelashes_eyebrows, eyelashes_eyebrows_root)

        # Ресницы и брови => Наращивание уголков
        try:
            increase_angles_root = Services.objects.get(name="Наращивание уголков", parent=eyelashes_eyebrows_root)
            print(f'Услуга "{increase_angles_root}" уже существует')
        except Exception as e:
            increase_angles_root = Services.objects.create(name="Наращивание уголков", parent=eyelashes_eyebrows_root)
            print(f'Услуга "{increase_angles_root}" создана!')

        increase_angles = [
            'Неполный объем',
            'Наращивание 1D',
            'Наращивание 2D',
            'Наращивание 3D',
            'Наращивание 4D',
            'Наращивание 5D',
        ]

        self._createSubServices(increase_angles, increase_angles_root)


    def addSalons(self):
        salons_count = Salon.objects.all().count()
        if salons_count == 0:
            i = 1
            for _ in range(20):
                salon = Salon(active=True, \
                                name=f"Salon name {i}", \
                                description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris molestie nisl erat, in auctor purus vehicula vel. Mauris pharetra maximus sapien non bibendum. Pellentesque placerat mauris at dictum lobortis. Nulla consectetur tortor at magna faucibus suscipit. Vivamus aliquam lorem sem, in porta orci commodo sit amet.", \
                                phone="+79990001100", \
                                email="salonmail@gmail.com", \
                                site_url="https://google.com"
                            )
                salon.save()
                print(f"Салон {salon.name} создан")
                i += 1


    def addSalonsWorkSchedules(self):
        # salons = Salon.objects.all()
        addresses = Address.objects.all()
        hours_range = ["11", "15", "18"]

        if addresses.count() > 0:
            for address in addresses:
                i = 0
                if not WorkSchedule.objects.filter(address=address).exists():
                    for _ in range(7):
                        # salon_instance = Salon.objects.get(id=salon.id)
                        address_instance = Address.objects.get(id=address.id)
                        ws = WorkSchedule(address=address_instance, \
                                            week_day=WorkSchedule.WEEK_DAYS[i][0], \
                                            # working_hours_from="09:00:00", \
                                            # working_hours_to="18:00:00", \
                                            working_hours_to=f"{random.choice(hours_range)}:00:00", \
                                        )
                        ws.save()
                        print(f'Рабочий график для салона "{ws.address}" на {ws.get_week_day_display()} создан')
                        i += 1
                else:
                    print(f'Рабочий график для салона "{address}" уже существует')


    def addCity(self):
        cities_list = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Нижний Новгород', 'Краснодар']

        if City.objects.all().count() == 0:
            for сity_name in cities_list:
                try:
                    city = City.objects.get(city=сity_name)
                    print(f'Город "{city.name}" уже существует')
                except Exception as e:
                    city = City(name=сity_name)
                    city.save()
                    print(f'Город "{city.name}" создан!')
        else:
            print(f'Города уже созданы!')


    def addMetro(self):
        # Москва
        moscow_metro_stations_list = ['Авиамоторная', 'Автозаводская (14 линия)', 'Автозаводская (Замоскворецкая линия)', 'Академическая', 'Алексеевская', 'Алма-Атинская', 'Алтуфьево', 'Андроновка', 'Аннино', 'Арбатская (Арбатско-Покровская линия)', 'Арбатская (Филевская линия)', 'Аэропорт', 'Бабушкинская', 'Багратионовская', 'Балтийская', 'Баррикадная', 'Бауманская', 'Беговая', 'Белокаменная', 'Белорусская', 'Беляево', 'Бибирево', 'Библиотека им. Ленина', 'Битцевский парк', 'Борисово', 'Боровицкая', 'Ботанический сад', 'Ботанический сад (14 линия)', 'Братиславская', 'Бульвар Адмирала Ушакова', 'Бульвар Дмитрия Донского', 'Бульвар Рокоссовского', 'Бунинская аллея', 'Бутырская', 'Варшавская', 'ВДНХ', 'Верхние Котлы', 'Владыкино', 'Владыкино (14 линия)', 'Водный стадион', 'Войковская', 'Волгоградский проспект', 'Волжская', 'Волоколамская', 'Воробьевы горы', 'Выставочная', 'Выставочный центр', 'Выхино', 'Деловой центр', 'Деловой центр (МЦК)', 'Динамо', 'Дмитровская', 'Добрынинская', 'Домодедовская', 'Достоевская', 'Дубровка', 'Дубровка (14 линия)', 'Жулебино', 'ЗИЛ', 'Зорге', 'Зябликово', 'Измайлово', 'Измайловская', 'Калужская', 'Кантемировская', 'Каховская', 'Каширская', 'Киевская', 'Китай-город', 'Кожуховская', 'Коломенская', 'Комсомольская', 'Коньково', 'Коптево', 'Котельники', 'Красногвардейская', 'Краснопресненская', 'Красносельская', 'Красные Ворота', 'Крестьянская застава', 'Кропоткинская', 'Крылатское', 'Крымская', 'Кузнецкий мост', 'Кузьминки', 'Кунцевская', 'Курская', 'Кутузовская', 'Ленинский проспект', 'Лермонтовский проспект', 'Лесопарковая', 'Лихоборы', 'Локомотив', 'Ломоносовский проспект', 'Лубянка', 'Лужники', 'Люблино', 'Марксистская', 'Марьина роща', 'Марьино', 'Маяковская', 'Медведково', 'Международная', 'Менделеевская', 'Минская', 'Митино', 'Молодежная', 'Мякинино', 'Нагатинская', 'Нагорная', 'Нахимовский проспект', 'Нижегородская', 'Новогиреево', 'Новокосино', 'Новокузнецкая', 'Новослободская', 'Новохохловская', 'Новоясеневская', 'Новые Черемушки', 'Окружная', 'Октябрьская', 'Октябрьское поле', 'Орехово', 'Отрадное', 'Охотный ряд', 'Павелецкая', 'Панфиловская', 'Парк Культуры', 'Парк Победы', 'Партизанская', 'Первомайская', 'Перово', 'Петровский парк', 'Петровско-Разумовская', 'Печатники', 'Пионерская', 'Планерная', 'Площадь Гагарина', 'Площадь Ильича', 'Площадь Революции', 'Полежаевская', 'Полянка', 'Пражская', 'Преображенская площадь', 'Пролетарская', 'Проспект Вернадского', 'Проспект Мира', 'Профсоюзная', 'Пушкинская', 'Пятницкое шоссе', 'Раменки', 'Речной вокзал', 'Рижская', 'Римская', 'Ростокино', 'Румянцево', 'Рязанский проспект', 'Савеловская', 'Саларьево', 'Свиблово', 'Севастопольская', 'Семеновская', 'Серпуховская', 'Славянский бульвар', 'Смоленская (Арбатско-Покровская линия)', 'Смоленская (Филевская линия)', 'Сокол', 'Соколиная гора', 'Сокольники', 'Спартак', 'Спортивная', 'Сретенский бульвар', 'Стрешнево', 'Строгино', 'Студенческая', 'Сухаревская', 'Сходненская', 'Таганская', 'Тверская', 'Театральная', 'Текстильщики', 'Телецентр', 'Теплый Стан', 'Технопарк', 'Тимирязевская', 'Третьяковская', 'Тропарево', 'Трубная', 'Тульская', 'Тургеневская', 'Тушинская', 'Угрешская', 'Улица 1905 года', 'Улица Академика Королёва', 'Улица Академика Янгеля', 'Улица Горчакова', 'Улица Милашенкова', 'Улица Сергея Эйзенштейна', 'Улица Скобелевская', 'Улица Старокачаловская', 'Университет', 'Филевский парк', 'Фили', 'Фонвизинская', 'Фрунзенская', 'Хорошево', 'Хорошевская', 'Царицыно', 'Цветной бульвар', 'ЦСКА', 'Черкизовская', 'Чертановская', 'Чеховская', 'Чистые пруды', 'Чкаловская', 'Шаболовская', 'Шелепиха', 'Шипиловская', 'Шоссе Энтузиастов', 'Щелковская', 'Щукинская', 'Электрозаводская', 'Юго-Западная', 'Южная', 'Ясенево']

        city_moscow_instance = City.objects.get(name="Москва")

        if Metro.objects.filter(city=city_moscow_instance).count() == 0:
            for mm_station in moscow_metro_stations_list:
                try:
                    metro = Metro.objects.get(city=city_moscow_instance, name=mm_station)
                    print(f'Станция метро "{metro.name}" в городе {metro.city} уже существует')
                except Exception as e:
                    metro = Metro(city=city_moscow_instance, name=mm_station)
                    metro.save()
                    print(f'Станция метро "{metro.name}" в городе {metro.city} создана!')
        else:
            print("Метро в Москве создано")


    def addAddress(self):
        if Address.objects.all().count() == 0:
            city_moscow_instance = City.objects.get(name="Москва")

            for salon_instance in Salon.objects.all():
                # salon_random_instance = Salon.objects.filter(active=True).order_by('?').first()

                # Create two addresses for Salon
                for _ in range(2):
                    metro_random_instance = Metro.objects.all().order_by('?').first()
                    address = Address(salon=salon_instance, \
                                        city=city_moscow_instance, \
                                        metro=metro_random_instance, \
                                        street=f'{random.choice(["ул. Большая Ордынка", "пр. Вернадского", "ул. Воздвиженка", "Покровский бульвар"])}', \
                                        building=f'{random.randint(1,50)}', \
                                        latitude=f'55.{random.randint(510000,740000)}', \
                                        longitude=f'37.{random.randint(570000,810000)}', \
                                    )
                    address.save()
                    print(f'Адрес {address.city} {address.metro} {address.street} {address.building} создан')
        else:
            print("Адреса созданы")


    def addSalonsEmployees(self):
        surnames_arr = ['Иванов', 'Петров', 'Сидоров', 'Андреев', 'Лебедев']
        names_arr = ['Иван', 'Кирилл', 'Игорь', 'Артем', 'Павел']
        patronymics_arr = ['Иванович', 'Алексеевич', 'Игоревич', 'Семенович', 'Владимирович']

        salons = Salon.objects.all()
        for salon in salons:
            i = 0
            if not Employee.objects.filter(salon=salon).exists():
                for _ in range(10):
                    salon_obj = Salon.objects.get(id=salon.id)
                    employee = Employee(active=True, \
                                        salon=salon_obj, \
                                        surname=random.choice(surnames_arr), \
                                        name=random.choice(names_arr), \
                                        patronymic=random.choice(patronymics_arr), \
                                    )
                    employee.save()
                    # Set Services by it's id's
                    employee.services.set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                    print(f'Сотрудник {employee.surname} {employee.name} {employee.patronymic} создан')
            else:
                print(f'Сотрудник уже существует')


    def addSalonServices(self):
        salons = Salon.objects.all()
        # addresses = Address.objects.all()
        services_ids_list = Services.objects.all().values_list('id', flat=True)
        # services_ids_list_random = random.sample(list(services_ids_list), 10)

        for salon in salons:
            salon_instance = Salon.objects.get(id=salon.id)
            address_instance = Address.objects.filter(salon=salon_instance).first()

            services_ids_list_random = random.sample(list(services_ids_list), 10)

            # for service_id in services_ids_list:
            for service_id in services_ids_list_random:
                service_instance = Services.objects.get(id=service_id)
                salon_service = SalonServices(salon=salon_instance, \
                                            address=address_instance, \
                                            service=service_instance, \
                                            price=random.randint(900,9000)
                                            )
                salon_service.save()
                print(f'Услуга "{service_instance.name}" для Салона "{salon.name}", с ценой {salon_service.price} создана!')


    def addClient(self):
        salons_ids_list = list(Salon.objects.all().values_list('id', flat=True))

        if Client.objects.all().count() == 0:
            for salon_id in salons_ids_list:
                salon_instance = Salon.objects.get(id=salon_id)

                for _ in range(15):
                    client = Client(active=True, \
                                    salon=salon_instance, \
                                    phone=f'7988{random.randint(0000000,9999999)}', \
                                    first_name=f'Клиент_{salon_instance.name.lower()}', \
                                    )
                    client.save()
                    print(f'Клиент Салона "{salon_instance.name}" создана!')
        else:
            print("Клиенты салонов уже созданы")


    def addClientAppointments(self):
        users_client = Account.objects.filter(groups__name='Client')

        for user in users_client:
            user_instance = Account.objects.get(id=user.id)
            employee_instance = Employee.objects.get(id=random.choice([1, 2, 3]))
            salon_instance = Salon.objects.get(id=random.choice([1, 2, 3]))

            if ClientAppointment.objects.all().count() == 0:
                for _ in range(5):
                    client_appointment = ClientAppointment(client=user_instance, \
                                                            employee=employee_instance, \
                                                            # datetime="2020-08-14 16:30:00", \
                                                            datetime=timezone.now(), \
                                                            status="in_progress", \
                                                            comment="Some client comment", \
                                                        )
                    client_appointment.save()

                    services_ids_list = Services.objects.all().values_list('id', flat=True)
                    # client_appointment.services.set(["1", "2", "3"])
                    client_appointment.services.set([str(random.choice(services_ids_list)), str(random.choice(services_ids_list)), str(random.choice(services_ids_list))])
                    print(f"Запись в салон {client_appointment.id} создана!")
            else:
                print("Записи Клиентов в Салон уже созданы")


    def addActions(self):
        # Get five random Salons
        salons = Salon.objects.filter(active=True).order_by('?')[:5]

        if Actions.objects.all().count() == 0:
            for salon in salons:
                salon_instance = Salon.objects.get(id=salon.id)
                service_instance = Services.objects.get(id=4)

                i = 1
                for _ in range(5):
                    action = Actions(active=True, \
                                        action_type="0", \
                                        salon=salon_instance, \
                                        services=service_instance, \
                                        title=f"Акция {i}", \
                                        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris molestie nisl erat, in auctor purus vehicula vel. Mauris pharetra maximus sapien non bibendum. Pellentesque placerat mauris at dictum lobortis. Nulla consectetur tortor at magna faucibus suscipit. Vivamus aliquam lorem sem, in porta orci commodo sit amet.", \
                                        discount=15, \
                                    )
                    action.save()
                    print(f"Акция для {action.title} Салона {action.salon.name} создана!")
                    i += 1
        else:
            print("Акции уже созданы")


    # Init creation
    def createDummyContent(self):
        self.addServices()

        self.addSalons()

        self.addCity()
        self.addMetro()
        self.addAddress()

        self.addSalonsWorkSchedules()
        self.addSalonsEmployees()
        self.addSalonServices()
        self.addActions()
        self.addClient()
        # self.addClientAppointments()