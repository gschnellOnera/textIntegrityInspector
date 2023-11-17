FROM python:3.8-slim

RUN pip install  -i ${PYPI_SERVER}/simple --no-cache-dir --upgrade pip pipenv

RUN  --mount=type=bind,target=/tmp \
    cd /tmp && \
    pipenv install --deploy --verbose --system && \
    pipenv --clear

CMD [ python -m ]