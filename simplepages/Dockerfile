FROM python:3.3.6-wheezy

EXPOSE 80

ENV FLASK_APP "src/app.py"
ENV FLASK_DEBUG "true"

WORKDIR /app

# Install any needed packages specified in requirements.txt
Add ./requirements.txt /app/
RUN pip install -r requirements.txt

# Copy source code into the image
ADD ./simplepages /app/src
