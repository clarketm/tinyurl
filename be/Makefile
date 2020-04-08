-include ../Makefile.common.mk

HUB := clarketm
PROJECT := tinyurl-be
PYTHON := python3
CORES := $(shell expr "2" "*" "$(shell getconf _NPROCESSORS_ONLN || 1)" "+" "1")
VERSION := 1.0.0
PORT := 8000

.PHONY: dev install
dev install:
ifeq (, $(shell which pipenv))
	python3 -m pip install -r requirements-dev.txt
else
	pipenv install --dev
endif

.PHONY: create-venv
create-venv:
ifeq (, $(shell which pipenv))
	test -d venv || $(PYTHON) -m venv venv
endif

.PHONY: venv
venv: create-venv
ifeq (, $(shell which pipenv))
	@echo $(shell realpath ./venv/bin/activate) | tee >(pbcopy)
else
	@echo $(shell pipenv --venv)/bin/activate | tee >(pbcopy)
endif

.PHONY: requirements
requirements:
	pipenv lock --requirements | sed '1,2d' > requirements.txt
	pipenv lock --dev --requirements | sed '1,2d' > requirements-dev.txt

.PHONY: format
f format:
	$(PYTHON) -m black . -l 150

.PHONY: docstring
docstring:
	pyment -w ./tinyurl

.PHONY: start-dev
start-dev:
	uvicorn --host=0.0.0.0 --port=${PORT} app.main:app --reload

.PHONY: start
start:
	gunicorn -b 0.0.0.0:${PORT} -k uvicorn.workers.UvicornWorker -w ${CORES} -t 900 app.main:app

.PHONY: test
test:
	$(PYTHON) -m pytest **/*_test.py --quiet

.PHONY: test-envs
test-envs:
	pyenv local 3.5.6 3.6.8 3.7.7 system
	$(PYTHON) -m tox

.PHONY: test-cov
test-cov:
	$(PYTHON) -m pytest tests --quiet --cov=api_tools --cov-report=html --cov-report=term --show-capture=all

.PHONY: image
image:
	docker build -t "$(HUB)/$(PROJECT):latest" -t "$(HUB)/$(PROJECT):$(VERSION)" .

.PHONY: push
push:
	docker push "$(HUB)/$(PROJECT):latest"
	docker push "$(HUB)/$(PROJECT):$(VERSION)"
