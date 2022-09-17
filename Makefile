.PHONY: default format mypy build push test tox


IMAGE_NAME := pytoolkit
PROJECT_NAME := pytoolkit

default: build push

format: refactor pre-commit

refactor:
	@yapf -r -i . 
	@isort . 
	@pycln -a .

pre-commit:
	@pre-commit run --all-file

mypy:
	@mypy .

build:
	docker build --platform linux/amd64 -t $(IMAGE_NAME) .

push:
	docker push $(IMAGE_NAME)
	if [ -n ${BARK_TOKEN} ]; then curl https://api.day.app/$(BARK_TOKEN)/$(PROJECT_NAME)%20push%20success; fi;

tox:
	docker volume create pytoolkit-tox-testenv
	docker build -t pytoolkit-tox-testenv -f ./tox.Dockerfile .
	docker run -it --rm -v pytoolkit-tox-testenv:/app/.tox pytoolkit-tox-testenv
	if [ -n ${BARK_TOKEN} ]; then curl https://api.day.app/$(BARK_TOKEN)/$(PROJECT_NAME)%20tox%20success; fi;
