FROM python:3.8-slim

RUN mkdir /data

RUN pip install  -i ${PYPI_SERVER}/simple --no-cache-dir --upgrade pip pipenv

RUN  --mount=type=bind,target=/tmp \
    cd /tmp && \
    pipenv install --dev --deploy --verbose --system && \
    pipenv --clear

WORKDIR /data

CMD [ python -m textIntegrityInspector ]