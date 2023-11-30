FROM python:3.8-slim

RUN mkdir /data

RUN  --mount=type=bind,target=/tmp \
    cd /tmp && \
    pip install  --no-cache-dir  .

# RUN pip install  --no-cache-dir --upgrade pip pipenv
# 
# RUN  --mount=type=bind,target=/tmp \
#     cd /tmp && \
#     pipenv install --dev --deploy --verbose --system && \
#     pipenv --clear

WORKDIR /data

ENTRYPOINT [ "python", "-m", "textIntegrityInspector" ]

ARG CI_COMMIT_SHA=""
LABEL commit_sha1="${CI_COMMIT_SHA}"