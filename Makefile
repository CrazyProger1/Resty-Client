.PHONY: test
test:
	poetry run python -m pytest tests/

.PHONY: build
build:
	poetry build


.PHONY: coverage
coverage:
	poetry run coverage run -m pytest tests/


.PHONY: coverage-report
coverage-report: coverage;
	poetry run coverage report -m


.PHONY: format
format:
	poetry run python -m black tests
	poetry run python -m black --exclude "types.py" resty
	poetry run python -m black examples