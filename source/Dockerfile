# pull official base image
FROM python:3.8.0-alpine

# copy project
COPY . /usr/src/app/
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#FROM library/postgres
#ENV POSTGRES_USER loh
#ENV POSTGRES_PASSWORD pidr
#ENV POSTGRES_DB govno

# install dependencies
#COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apk add --virtual muk python3-dev musl-dev gcc zlib-dev jpeg-dev postgresql-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

## copy project
#COPY . /usr/src/app/

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]