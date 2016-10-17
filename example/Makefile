deps:
	pip install -r requirements.txt

deps-dev:
	pip install -r requirements-dev.txt

app-server-dev:
	cd app_server && python -m http.server 7777 && cd ..

init-db-sample-data:
	python scripts/init_db_sample_data.py
	rm .brome.pkl
