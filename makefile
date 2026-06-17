.PHONY: build run stop logs shell

build:
	docker build -t airflow-test-1 .

run:
	docker run -p 8080:8080 -v $(PWD)/dags:/opt/airflow/dags airflow-test-1 standalone

run-detached:
	docker run -d -p 8080:8080 -v $(PWD)/dags:/opt/airflow/dags --name airflow airflow-test-1 standalone

stop:
	docker stop airflow && docker rm airflow

logs:
	docker logs -f airflow

shell:
	docker exec -it airflow bash
