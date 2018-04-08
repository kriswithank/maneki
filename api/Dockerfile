FROM python:3.3.6-wheezy

EXPOSE 80

ENV FLASK_APP "api.wsgi"

WORKDIR /app

# Copy package files into image
ADD . /app/api

# Install required pip packages from requirements.txt
RUN pip install -r /app/api/requirements.txt

# Install the api package and allow modifications
RUN pip install -e ./api
