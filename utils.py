import json
import sqlite3


def look_for_title(query):
    """Возвращает словарь с данными последнего вышедшего фильма,
    в названии которого содержится искомое слово
    Args:
        query: искомое слово"""
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute(f"SELECT `title`, `country`, MAX(release_year), `listed_in`, `description` "
                    f"FROM netflix "
                    f"WHERE title LIKE '% {query} %'")
        result = cur.fetchall()
        if result[0][0] is None:
            return None
        dict_result = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][4]
        }
        return dict_result


def get_movie_by_year(start, finish):
    """Возвращает список из 100 фильмов, расположенных в заданном временном диапазоне
    Args:
        start: год, начало диапазона
        finish: год, конец диапазона"""
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute(f"SELECT `title`, `release_year` "
                    f"FROM netflix "
                    f"WHERE release_year BETWEEN {start} AND {finish} "
                    f"LIMIT 100")
        result = cur.fetchall()
        list_result = []
        for i in range(len(result) - 1):
            new_dict = {"title": result[i][0],
                        "release_year": result[i][1]}
            list_result.append(new_dict)
        return list_result


def get_movie_by_rating(rating):
    """Возвращает список фильмов с рейтингом, заданным ключевым словом:
    children - 'G'
    family - 'G, PG, PG-13'
    adult - 'R, NC-17'
    Args:
        rating: ключевое слово для поиска по рейтингу"""
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        if rating.lower() == 'children':
            cur.execute(f"SELECT `title`, `rating`, `description` "
                        f"FROM netflix "
                        f"WHERE rating=='G'")
        elif rating.lower() == 'family':
            cur.execute(f"SELECT `title`, `rating`, `description` "
                        f"FROM netflix "
                        f"WHERE rating IN ('G', 'PG', 'PG-13')")
        elif rating.lower() == 'adult':
            cur.execute(f"SELECT `title`, `rating`, `description` "
                        f"FROM netflix "
                        f"WHERE rating IN ('R', 'NC-17')")
        else:
            return "there is no such rating. Please, try again using another keyword."
        result = cur.fetchall()
        list_result = []
        for i in range(len(result) - 1):
            new_dict = {"title": result[i][0],
                        "rating": result[i][1],
                        "description": result[i][2]}
            list_result.append(new_dict)
        return list_result


def get_movie_by_genre(genre):
    """Возвращает список из 10 самых 'свежих' фильмов с заданным жанром
    Args:
        genre: искомый жанр"""
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute("SELECT `title`, `description` "
                    "FROM netflix "
                    f"WHERE listed_in LIKE '% {genre} %' "
                    "ORDER BY release_year DESC "
                    "LIMIT 10")
        result = cur.fetchall()
        if result is None:
            return "there is no such genre. Please, try again using another keyword."
        list_result = []
        for i in range(len(result) - 1):
            new_dict = {"title": result[i][0],
                        "description": result[i][1]}
            list_result.append(new_dict)
        return list_result


def get_movie_by_params(type_m, year, genre):
    """Возвращает список фильмов/сериалов с заданным типом, годом и жанром
    Args:
        type_m: тип (фильм или сериал)
        year: год выпуска
        genre: жанр"""

    list_result = []

    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute("SELECT `title`, `description` "
                    "FROM netflix "
                    f"WHERE listed_in LIKE '%{genre}%' "
                    f"AND type=='{type_m}' "
                    f"AND release_year=={year}")
        result = cur.fetchall()

    for i in range(len(result) - 1):
        new_dict = {"title": result[i][0],
                    "description": result[i][1]}
        list_result.append(new_dict)

    return json.dumps(list_result)


def get_movie_with_actors(actor_1, actor_2):
    """Сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз
        Args:
            actor_1: имя первого актёра
            actor_2: имя второго актёра"""
    actors = []
    result_list = []

    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute("SELECT DISTINCT `cast` "
                    "FROM netflix "
                    f"WHERE `cast` LIKE '%{actor_1}%{actor_2}%'")

        result = cur.fetchall()

    for i in range(len(result) - 1):
        actors_line = result[i][0].split(', ')
        for x in range(len(actors_line)):
            if actors_line[x] != actor_1 and actors_line[x] != actor_2:
                actors.append(actors_line[x])

    for i in range(len(actors)):
        if actors.count(actors[i]) >= 2 and actors[i] not in result_list:
            result_list.append(actors[i])

    return result_list
