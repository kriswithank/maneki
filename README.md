# maneki
Personal website

### Running the website:

Runs gunicorn in production and the built in flask dev server in the
development envronment.

To run the development server:

```
docker-compose up
```

For the production server:

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
