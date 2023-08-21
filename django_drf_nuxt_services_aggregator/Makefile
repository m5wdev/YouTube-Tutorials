start_migrate:
	docker-compose run backend python manage.py migrate --noinput
create_user:

	docker-compose run backend python manage.py createsuperuser

generate:
    docker-compose run backend python manage.py generate_content -q 100


run_dev:
	docker-compose --file docker-compose.dev.yml up

build_dev:
	docker-compose --file docker-compose.dev.yml up --build
