.PHONY: default format mypy precommit export tox tox362



default: format

export:
	@poetry export -o requirements.txt --all-extras --with-credentials

format: precommit

refactor:
	@ruff check . --fix
	@ruff format .

precommit:
	@pre-commit install
	@pre-commit run --all-file

mypy:
	@mypy .

tox:
	@docker volume create pytoolkit-tox-testenv
	@docker build -t pytoolkit-tox-testenv -f ./tox.Dockerfile .
	@make export 
	@docker run -it --rm -v pytoolkit-tox-testenv:/app/.tox -v $(PWD)/requirements.txt:/app/requirements.txt  pytoolkit-tox-testenv
	@rm ./requirements.txt

tox370:
	@docker volume create pytoolkit-tox-testenv
	@docker build -t pytoolkit-tox-testenv -f ./tox.Dockerfile .
	@make export 
	@docker run -it --rm -v pytoolkit-tox-testenv:/app/.tox -v $(PWD)/requirements.txt:/app/requirements.txt  pytoolkit-tox-testenv tox -e py37
	@rm ./requirements.txt
