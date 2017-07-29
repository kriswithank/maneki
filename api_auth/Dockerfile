FROM python:3.3.6-wheezy

EXPOSE 80

ENV FLASK_APP "api_auth.wsgi"

WORKDIR /app

# Copy package files into image
ADD . /app/api_auth

# Install required pip packages from requirements.txt
RUN pip install -r /app/api_auth/requirements.txt

# Install the api_auth package and allow modifications
RUN pip install -e ./api_auth
