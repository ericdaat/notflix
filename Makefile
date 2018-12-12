POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=recommender
HOST=127.0.0.1

install:
	rm -rf venv; \
	virtualenv venv; \
	source venv/bin/activate; \
 	pip install -r requirements.txt; \
	echo "done"; \


init-db: export PYTHONPATH="$(shell pwd)/src/"
init-db:
	docker-compose up -d postgres; \
	source venv/bin/activate; \
	cd src; \
	python admin/init-db.py; \
	echo "done"; \

