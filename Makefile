.PHONY: default format mypy build push test precommit export tox tox362



default: format

export:
	@poetry export -o requirements.txt --all-extras --with-credentials

format: refactor precommit

refactor:
	@yapf -r -i . 
	@isort . 
	@pycln -a .

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

tox362:
	@docker volume create pytoolkit-tox-testenv
	@docker build -t pytoolkit-tox-testenv -f ./tox.Dockerfile .
	@make export 
	@docker run -it --rm -v pytoolkit-tox-testenv:/app/.tox -v $(PWD)/requirements.txt:/app/requirements.txt  pytoolkit-tox-testenv tox -e py3.6.2
	@rm ./requirements.txt
