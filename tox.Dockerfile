FROM qsoyq/python-tox-testenv

EXPOSE 8000

ENV TZ=Asia/Shanghai

WORKDIR /app

RUN pip install tox

ENV PYTHONPATH="/app:${PYTHONPATH}"

COPY pyproject.toml pyproject.toml

COPY poetry.lock poetry.lock

COPY pytoolkit /app/pytoolkit

COPY tests /app/tests

CMD tox
