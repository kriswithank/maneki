[![Build Status](https://travis-ci.org/kriswithank/maneki.svg?branch=master)](https://travis-ci.org/kriswithank/maneki)

# maneki
A modular website for personal use

### Running the website:

There are two steps to getting the website running: setting up the
database and running the server.

---

##### Setting up the database

There are two commmand you can run to minipulate the databse.

You can drop all of the tables in the database with

```
docker-compose run api-finances flask dropdb
docker-compose run api_auth flask dropdb
```

And you can create empty tables in the database with

```
docker-compose run api-finances flask initdb
docker-compose run api_auth flask initdb
```

Currently only the api-finances and api_auth service talks to the database and
the currently share the same database, but in the future, every service should
have it's own database and so you would have to repeat these commands on a
per-service basis.

---

##### Running the server

Nginx is used in both production and development, underneath this
gunicorn is run in production and the built in flask development server
is run in the development envronment.

To run the development server:

```
docker-compose up
```

For the production server:

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
