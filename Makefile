SHELL:=$(shell which bash)

.PHONY: list
l h list help:
	@make -pq | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}' | sed '/Makefile/d' | sort

.PHONY: install
install:
	python3 -m pip install --upgrade -e .

.PHONY: install-dev
install-dev:
	python3 -m pip install --upgrade -e .[dev]

.PHONY: dev
dev:
ifeq (, $(shell which pipenv))
	python3 -m pip install -r requirements-dev.txt
else
	pipenv install --dev
endif
	hooks

.PHONY: hooks precommit
hooks precommit:
	cp ./hooks/pre-commit $(shell  git rev-parse --git-path hooks)

.PHONY: create-venv
create-venv:
ifeq (, $(shell which pipenv))
	test -d venv || python3 -m venv venv
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
	python3 -m black . -l 150

.PHONY: build
build: clean
	rm -rf ./dist/*
	python3 setup.py sdist bdist_wheel

.PHONY: requirements
requirements:
	pipenv lock --requirements | sed '1,2d' > requirements.txt
	pipenv lock --dev --requirements | sed '1,2d' > requirements-dev.txt

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

.PHONY: docstring
docstring:
	pyment -w ./tinyurl

.PHONY: test
test:
	python3 -m pytest tests --quiet

.PHONY: test-envs
test-envs:
	pyenv local 3.5.6 3.6.8 3.7.7 system
	python3 -m tox

.PHONY: test-cov
test-cov:
	python3 -m pytest tests --quiet --cov=api_tools --cov-report=html --cov-report=term --show-capture=all

.PHONY: clean
clean:
	rm -rf ./dist ./build ./*.egg-info ./htmlcov ./.pytest_cache
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: check
check:
	twine check dist/*

.PHONY: build-hash
build-hash:
	mkdir -p ./config
	git rev-parse --short=7 HEAD > ./config/BUILD

.PHONY: deploy
deploy:
	@echo "TODO:

.PHONY: upload-test
upload-test: test clean build check
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
publish upload: test clean build check
	twine upload dist/*

