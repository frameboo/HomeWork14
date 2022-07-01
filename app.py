import json
from flask import Flask
import utils

app = Flask(__name__)


@app.get('/movie/<title>')
def search_by_title_view(title):
    result = utils.search_by_title(title=title)
    return app.response_class(
            response=json.dumps(result, ensure_ascii=False, indent=4),
            mimetype="application/json")


@app.get('/movie/<year1>/to/<year2>')
def search_by_year_view(year1, year2):
    result = utils.search_by_year(year1=year1, year2=year2)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        mimetype="application/json")


@app.get('/rating/<rating>')
def search_by_rating_view(rating):
    result = utils.search_by_rating(rating=rating)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        mimetype="application/json")


@app.get('/genre/<genre>')
def search_by_genre_view(genre):
    result = utils.search_by_genre(genre=genre)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True)
