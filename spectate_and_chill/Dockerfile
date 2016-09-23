FROM continuumio/anaconda3
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
