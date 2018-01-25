FROM python:3.6.4-jessie

EXPOSE 80

ENV FLASK_APP "finances.wsgi"
ENV FLASK_DEBUG "true"

WORKDIR /app

# Copy package files into image
ADD . /app/finances

# Install required pip packages from requirements.txt
RUN pip install -r /app/finances/requirements.txt

# Install the finances package and allow modifications
RUN pip install -e ./finances
