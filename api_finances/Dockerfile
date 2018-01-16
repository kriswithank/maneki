FROM python:3.6.4-jessie

EXPOSE 80

ENV FLASK_APP "api_finances.wsgi"
ENV FLASK_DEBUG "true"

WORKDIR /app

# Copy package files into image
ADD . /app/api_finances

# Install required pip packages from requirements.txt
RUN pip install -r /app/api_finances/requirements.txt

# Install the api_finances package and allow modifications
RUN pip install -e ./api_finances
