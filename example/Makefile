deps:
	pip install -r requirements.txt

deps-dev:
	pip install -r requirements-dev.txt

start-app-server-prod:
	scripts/start_app_server.sh

stop-app-server-prod:
	scripts/stop_app_server.sh

app-server-dev:
	cd app_server && python -m http.server 7777 && cd ..

test-prod:
	py.test webbaseserver/tests --instafail --html=last-report.html

query:
	python scripts/query.py

reset-db:
	python scripts/reset_db.py
	rm .brome.pkl

init-db-sample-data:
	python scripts/init_db_sample_data.py
	rm .brome.pkl
