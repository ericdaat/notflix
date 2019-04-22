#!make
SHELL=/bin/bash

include db-credentials.env
export $(shell sed 's/=.*//' db-credentials.env)

install:
	rm -rf venv; \
	virtualenv venv; \
	source venv/bin/activate; \
 	pip install -r requirements.txt; \
 	docker-compose build; \
 	cp -n db-credentials.env.dist db-credentials.env; \
	echo "done"; \

init-db:
	docker-compose stop api web; \
	docker-compose up -d postgres; \
	source venv/bin/activate; \
	PYTHONPATH="." POSTGRES_HOST="127.0.0.1" REDIS_HOST="127.0.0.1" \
		python -c "from src.data_interface import model; model.init()";  \
	echo "done"; \

insert-data:
	source venv/bin/activate; \
	PYTHONPATH="." POSTGRES_HOST="127.0.0.1" REDIS_HOST="127.0.0.1" \
		python src/scripts/init_notflix.py;  \
	echo "done"; \

start:
	docker-compose up -d web;

stop:
	docker-compose down;

docs:
	cd docs; \
	make clean; \
	find source/*.rst ! -name 'index.rst' -type f -exec rm -f {} +; \
	sphinx-apidoc ../ -o source -M; \
	make html;  \
	echo "done"; \

tests:
	docker-compose up -d postgres redis;
	source venv/bin/activate;
	PYTHONPATH="." POSTGRES_DB="test-db" \
		POSTGRES_HOST="127.0.0.1" REDIS_HOST="127.0.0.1" \
		python -m unittest discover -s tests;
