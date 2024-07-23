all: style run

style:
	isort app/ tests/ && black app/ tests/

run:
	python app/main.py