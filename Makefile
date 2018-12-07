docker run -v src -e PYTHONPATH=/src --env-file db-credentials.env -w /src \
recommender-system_python:latest\
python/admin/recommendations.py