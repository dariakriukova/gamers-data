FROM python:3.10-alpine

VOLUME [ "/data" ]
ENV DB=wwc_hb.db
ENV DATA_DIR=/data

RUN pip install pipenv --no-cache-dir
WORKDIR /code
COPY Pipfile* .
RUN pipenv install --system --deploy

ENV PYTHONPATH="${PYTHONPATH}:/code"
COPY src .
ENTRYPOINT [ "python", "./load.py" ]