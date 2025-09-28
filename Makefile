SRC_DIR = app

ifeq ($(OS),Windows_NT)
    MKDIR = mkdir
else
    MKDIR = mkdir -p
endif

.PHONY: create-htmlcov

create-htmlcov:
	$(MKDIR) htmlcov

clean:
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -f coverage.xml
	@rm -f coverage.html
	@rm -rf htmlcov/
	@rm -f *.log


flake8:
	flake8 --config ./devtools/config.ini

isort-check:
	isort -c --py 38 --profile=black -l 79 .

fix-python-import:
	isort --profile black --py 38 -m 3 --tc --up -l 79 .

check-python-import:
	isort --profile black -c --py 38 -m 3 --tc --up  -l 79 .

black:
	black --config ./devtools/config.toml .

black-check:
	black --config ./devtools/config.toml --check .

bandit:
	bandit -r -f custom ${SRC_DIR}

lint: fix-python-import black flake8

check-lint: check-python-import isort-check black-check bandit flake8

install:
	@echo "Setup envs"
	pip install pip-tools
	pip-compile requirements/base.in
	pip install -r requirements/base.txt

install-local:
	@echo "Setup envs local"
	pip install pip-tools
	pip-compile requirements/local.in
	pip install -r requirements/local.txt


coverage: clean create-htmlcov
	@py.test --cov=${SRC_DIR} --cov-report=html --cov-fail-under=90 tests/