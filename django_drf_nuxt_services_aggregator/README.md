# Service Centers Aggregator

[Frontend](#frontend)

[Backend](#backend)

[Генератор контента (в backend)](#генератор-контента-в-backend)

***

## Frontend

**Все команды выолняем в консоли, в директории frontend**

Install project

```bash
npm i
```

Run dev project

```bash
npm run dev
```

перейти по адресу http://localhost:3000/

***

## Backend

**Все команды выолняем в консоли, в директории backend**

Создать и активировать виртуальное окружение (если его нет)

```bash
python -m venv .env
```

```bash
source .env/bin/activate
```

Установить все пакеты

```bash
pip install -r requirements/requirements.txt
```

Запустить Django

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver

```

перейти по адресу http://localhost:8000/admin

***

## Генератор контента (в backend)

Все данные

```bash
python manage.py generate_content
```

флаг -q 500 (количество компаний)

```bash
python manage.py generate_content -q 500
```

под Docker

```bash
sudo docker-compose run backend python manage.py generate_content
```

```bash
sudo docker-compose run backend python manage.py generate_content -q 500
```
