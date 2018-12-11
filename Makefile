MYSQL_ROOT_PASSWORD=Pa$$w0rD
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_DATABASE=recommender
MYSQL_HOST=localhost

install:
	rm -rf venv; \
	virtualenv venv; \
    source venv/bin/activate; \
    pip install -r requirements.txt; \
	echo "done"; \


init-db: export PYTHONPATH="$(shell pwd)/src/"
init-db:
	docker-compose up -d mysql; \
    source venv/bin/activate; \
	cd src; \
	python admin/init_db.py; \
	echo "done"; \

