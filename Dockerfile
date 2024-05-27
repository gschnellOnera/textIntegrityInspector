FROM python:3.8-slim

RUN mkdir /data


RUN pip install  --no-cache-dir --upgrade pip pipenv

RUN  --mount=type=bind,target=/tmp \
    cd /tmp && \
    pipenv install --deploy --verbose --system && \
    pipenv --clear

RUN  --mount=type=bind,target=/tmp \
    cd /tmp && pip install  --no-cache-dir  dist/textIntegrityInspector-*.whl

WORKDIR /data
ENTRYPOINT [ "python", "-m", "textIntegrityInspector" ]

ARG CI_COMMIT_SHA=""
LABEL commit_sha1="${CI_COMMIT_SHA}"
