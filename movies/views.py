from flask import Blueprint, jsonify

from utils import *

movie_blueprint = Blueprint("movie_blueprint", __name__)


@movie_blueprint.route("/movie/<title>")
def search_title_page(title):
    """Поиск свежего фильма по ключевому слову в названии"""
    page = look_for_title(title)
    if not page:
        return "Фильм не найден"
    return jsonify(page)


@movie_blueprint.route("/movie/<int:start>/to/<int:finish>")
def search_year_page(start, finish):
    """Поиск фильмов по годам выпуска"""
    page = get_movie_by_year(start, finish)
    return jsonify(page)


@movie_blueprint.route("/rating/<rating>")
def search_rating_page(rating):
    """Поиск фильмов по рейтингу"""
    page = get_movie_by_rating(rating)
    return jsonify(page)


@movie_blueprint.route("/genre/<genre>")
def search_genre_page(genre):
    """Поиск фильмов по жанру"""
    page = get_movie_by_genre(genre)
    return jsonify(page)
