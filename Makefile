SHELL := $(shell which bash)
HUB = clarketm
PROJECT = tinyurl
VERSION := $(shell yq r ./deploy/Chart.yaml 'appVersion')
PYTHON := python3

.PHONY: list
l h list help:
	@make -pq | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sed '/Makefile/d' | sort

.PHONY: install
install:
	$(PYTHON) -m pip install --upgrade -e .

.PHONY: install-dev
install-dev:
	$(PYTHON) -m pip install --upgrade -e .[dev]

.PHONY: dev
dev:
ifeq (, $(shell which pipenv))
	$(PYTHON) -m pip install -r requirements-dev.txt
else
	pipenv install --dev
endif
	hooks

.PHONY: requirements
requirements:
	pipenv lock --requirements | sed '1,2d' > requirements.txt
	pipenv lock --dev --requirements | sed '1,2d' > requirements-dev.txt

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

.PHONY: format
f format:
	$(PYTHON) -m black . -l 150

.PHONY: docstring
docstring:
	pyment -w ./tinyurl

.PHONY: hooks precommit
hooks precommit:
	cp ./hooks/pre-commit $(shell  git rev-parse --git-path hooks)

.PHONY: hash
hash:
	mkdir -p ./config
	git rev-parse --short=7 HEAD > ./config/BUILD

.PHONY: start-dev
start-dev:
	uvicorn --host=0.0.0.0 --port=8000 main:app --reload

.PHONY: start
start:
	uvicorn --host=0.0.0.0 --port=8000 main:app
#	gunicorn -b 0.0.0.0:${PORT} -k eventlet -w ${CORES} -t 900 --reload api_tools.wsgi

.PHONY: start-docker
start-docker:
	docker-compose up

.PHONY: start-docker-dev
start-docker-dev:
	docker-compose -f docker-compose.dev.yml up

.PHONY: test
test:
	$(PYTHON) -m pytest *_test.py --quiet

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

.PHONY: deploy
deploy:
	helm install tinyurl ./deploy

