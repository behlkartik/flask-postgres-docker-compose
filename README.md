# flask-postgres-docker-compose

A simple REST API app using flask postgresql and docker-compose.

Run using:
> docker-compose up --build -d

API Endpoints:
> POST localhost:3000/api/movies -> create movie
> GET localhost:3000/api/casts -> create cast

> GET localhost:3000/api/movies -> get detailed list of all movies
> GET localhost:3000/api/movies/<id> -> get details of 1 movie
> GET localhost:3000/api/movie/<id>/cast -> get details of movie with cast
