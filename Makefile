.PHONY: format lint test qa

format:
	black .

lint:
	ruff check .

test:
	pytest -q

qa: format lint test
