from flask import Flask, jsonify, request
import os
import psycopg2
from dotenv import load_dotenv

CREATE_MOVIE_TABLE = "CREATE TABLE IF NOT EXISTS movie (id SERIAL PRIMARY KEY, name VARCHAR(20), duration VARCHAR(100), rating NUMERIC(4,2));"
CREATE_CAST_TABLE = "CREATE TABLE IF NOT EXISTS casts (id SERIAL PRIMARY KEY, actor_name VARCHAR(20), movie_id INTEGER, FOREIGN KEY (movie_id) REFERENCES  movie(id) ON DELETE CASCADE);"
INSERT_MOVIE_RETURN_ID = (
    "INSERT INTO movie(name, duration, rating) VALUES(%s, %s, %s) RETURNING id"
)
INSERT_CAST_RETURN_ID = (
    "INSERT INTO casts(actor_name, movie_id) VALUES(%s, %s) RETURNING id"
)
GET_MOVIE_WITH_ID = "SELECT * FROM movie WHERE id=(%s)"
GET_ALL_MOVIES = "SELECT * FROM movie"
GET_MOVIE_WITH_CAST = (
    "SELECT * FROM movie JOIN casts ON movie.id = casts.movie_id WHERE movie.id=(%s)"
)

load_dotenv()  # load env variables from .env to environment variables of process

app = Flask(__name__)
# db_url = os.getenv("DATABASE_URL")
db_name = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
connection = psycopg2.connect(
    dbname=db_name, user=user, password=password, host=db_host
)


def get_list_of_dict_from_cursor(cursor, type):
    if type == "one":
        movies = [
            dict(
                (cursor.description[i][0], value)
                for i, value in enumerate(cursor.fetchone())
            )
        ]
    else:
        movies = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
    return movies


def get_dict_from_cursor(cursor):
    movie = dict(
        (cursor.description[i][0], value) for i, value in enumerate(cursor.fetchone())
    )
    return movie


@app.before_first_request
def create_database():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT 'CREATE DATABASE {db_name}' \
                           WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{db_name}')"
            )
            cursor.execute(CREATE_MOVIE_TABLE)
            cursor.execute(CREATE_CAST_TABLE)


@app.post("/api/movies")
def create_movie():
    request_data = request.get_json()
    movie_name, movie_duration, movie_rating = (
        request_data["name"],
        request_data["duration"],
        request_data["rating"],
    )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                INSERT_MOVIE_RETURN_ID, (movie_name, movie_duration, movie_rating)
            )
            movie_id = cursor.fetchone()[0]
    return {"id": movie_id, "message": f"Movie with name {movie_name} created"}, 201


@app.get("/api/movies")
def get_movies():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_MOVIES)
            movies = get_list_of_dict_from_cursor(cursor, "all")
    return jsonify(movies), 200


@app.get("/api/movies/<int:movie_id>")
def get_movie_by_name(movie_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_MOVIE_WITH_ID, (movie_id,))
            movie = get_dict_from_cursor(cursor)
    return jsonify(movie), 200


@app.post("/api/casts")
def create_cast():
    request_data = request.get_json()
    actor_name, movie_id = request_data["actor_name"], request_data["movie_id"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_CAST_RETURN_ID, (actor_name, movie_id))
            cast_id = cursor.fetchone()[0]
    return {"id": cast_id, "message": f"Cast with actor_name {actor_name} created"}, 201


@app.get("/api/movie/<int:movie_id>/cast")
def get_movie_with_cast(movie_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_MOVIE_WITH_CAST, (movie_id,))
            movie = get_dict_from_cursor(cursor)
    return jsonify(movie), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000", debug=True)
