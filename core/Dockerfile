FROM python:3.9.2-alpine AS base
LABEL stage=builder

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk add --update \
    postgresql-dev \
    musl-dev \
    gcc \
    linux-headers

RUN pip install wheel && pip wheel --wheel-dir=/app/wheels -r requirements.txt

FROM python:3.9.2-alpine

COPY --from=base /app /app

WORKDIR /app

RUN apk add --update postgresql-libs && pip install --no-index --find-link=/app/wheels -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]