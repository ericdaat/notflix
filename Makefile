POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
HOST=

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
	python admin/init_db.py; \
	echo "done"; \

