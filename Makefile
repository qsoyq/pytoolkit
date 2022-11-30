.PHONY: default format mypy build push test tox


default: format

format: refactor pre-commit

refactor:
	@yapf -r -i . 
	@isort . 
	@pycln -a .

pre-commit:
	@pre-commit run --all-file

mypy:
	@mypy .

tox:
	docker volume create pytoolkit-tox-testenv
	docker build -t pytoolkit-tox-testenv -f ./tox.Dockerfile .
	docker run -it --rm -v pytoolkit-tox-testenv:/app/.tox pytoolkit-tox-testenv
	if [ -n ${BARK_TOKEN} ]; then curl https://api.day.app/$(BARK_TOKEN)/$(PROJECT_NAME)%20tox%20success; fi;
