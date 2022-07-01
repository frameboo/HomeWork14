import json
import sqlite3


def get_value_from_db(sql):
    """функция подключения БД"""

    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()
        return result


def search_by_title(title):
    """поиск по названию фильма, если таких названий несколько, то выводит самый свежий фильм"""

    sql = f'''select title, country, release_year, listed_in, description
              from netflix
              where title = '{title}'
              order by release_year desc
              limit 1'''
    result = get_value_from_db(sql)

    for item in result:
        return dict(item)


def search_by_year(year1, year2):
    """поиск по диапазону лет выпуска"""

    sql = f'''
                select title, release_year
                from netflix
                where release_year between '{year1}' and '{year2}'
                '''

    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))
    return result


def search_by_rating(rating):
    """поиск по рейтингу"""

    rating_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f'''
                select title, rating, description
                from netflix
                where rating in {rating_dict[rating]}
                '''

    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))
    return result


def search_by_genre(genre):
    """поиск по жанру"""

    sql = f'''
                select title, description
                from netflix
                where listed_in like '%{genre}%' 
                order by release_year desc
                limit 10
                '''

    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))
    return result


def search_pair_actors(actor1, actor2):
    """функция получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз"""

    sql = f'''
            select "cast"
            from netflix
            where "cast" like '%{actor1}%' and "cast" like '%{actor2}%'
            '''

    result = []
    actors_dict = {}

    for item in get_value_from_db(sql):
        actors = set(dict(item).get('cast').split(',')) - set([actor1, actor2])
        for actor in actors:
            actors_dict[str(actor).strip()] = actors_dict.get(str(actor).strip(), 0) + 1

    for key,value in actors_dict.items():
        if value >= 2:
            result.append(key)
    return result


def search_by_type_year_genre(film_type, year, genre):
    """функция, с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON"""

    sql = f'''
            select title, description
            from netflix
            where type = '{film_type}'
            and release_year = '{year}'
            and listed_in like '%{genre}%'
            '''

    result = []

    for item in get_value_from_db(sql):
        result.append(dict(item))
    return json.dumps(result, ensure_ascii=False, indent=4)


print(search_pair_actors('Rose McIver', 'Ben Lamb'))
print(search_by_type_year_genre('Movie', '2021', 'Documentaries'))
