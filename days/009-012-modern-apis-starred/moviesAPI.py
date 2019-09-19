import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


# helpers

def _load_movies_data():
    with open('movies.json') as f:
        movies = json.loads(f.read())
        return {movie["id"]: movie for movie in movies}


movies = _load_movies_data()
VALID_GENRES = set([movie["Genre"]
                         for movie in movies.values()])
MOVIE_NOT_FOUND = 'Movie not found'




# definition


class Movie(types.Type):
    id = validators.Integer(allow_null=True)  # assign in POST
    Movie = validators.String(max_length=150)
    Genre = validators.String(enum=list(VALID_GENRES))
    Year = validators.Integer(minimum=1900, maximum=2050)
    Language = validators.String(max_length=50, default='')


# API methods

def list_movies() -> List[Movie]:
    return [Movie(movie[1]) for movie in sorted(movies.items())]


def create_movie(movie: Movie) -> JSONResponse:
    movie_id = max(movies.keys())+1
    movie.id = movie_id
    movies[movie_id] = movie
    return JSONResponse(Movie(movie), status_code=201)


def get_movie(movie_id: int) -> JSONResponse:
    movie = movies.get(movie_id)
    if not movie:
        error = {'error': MOVIE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Movie(movie), status_code=200)


def update_movie(movie_id: int, movie: Movie) -> JSONResponse:
    if not movies.get(movie_id):
        error = {'error': MOVIE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    movie.id = movie_id
    movies[movie_id] = movie
    return JSONResponse(Movie(movie), status_code=200)


def delete_movie(movie_id: int) -> JSONResponse:
    if not movies.get(movie_id):
        error = {'error': MOVIE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del movies[movie_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_movies),
    Route('/', method='POST', handler=create_movie),
    Route('/{movie_id}/', method='GET', handler=get_movie),
    Route('/{movie_id}/', method='PUT', handler=update_movie),
    Route('/{movie_id}/', method='DELETE', handler=delete_movie),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
