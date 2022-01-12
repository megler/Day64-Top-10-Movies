# topTenMovies.py
#
# Python Bootcamp Day 64 - Top 10 Movies
# Usage:
#      A Flask app that lists your top 10 Movies.
#
# Marceia Egler January 12, 2022

import json
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from models import db
from forms import Movie_Rating, Movie_Title
from dotenv import dotenv_values
import requests, secrets

config = dotenv_values(".env")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
db.app = app
db.init_app(app)
with app.test_request_context():
    from models import Movie

    db.create_all()
Bootstrap(app)


@app.route("/")
def home():
    all_movies = Movie.query.filter().order_by(Movie.rating.asc())
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    update_form = Movie_Rating()
    movie_rating = update_form.movie_rating.data
    movie_review = update_form.movie_review.data
    movie_to_update = Movie.query.get(id)
    if request.method == "POST":
        movie_to_update.rating = movie_rating
        movie_to_update.review = movie_review
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html",
                           form=update_form,
                           id=id,
                           movie=movie_to_update)


@app.route("/delete/<id>")
def delete(id):
    movie_to_delete = Movie.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return render_template("delete.html", id=id)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_movie_form = Movie_Title()
    movie_title = add_movie_form.movie_title.data
    id = Movie.id
    if request.method == "POST":

        return redirect(url_for("select", title=movie_title))

    return render_template("add.html", form=add_movie_form)


@app.route("/select/<title>")
def select(title):
    params = {
        "api_key": config["MDB_API_KEY"],
        "query": title,
        "language": "en-US"
    }

    movie_search = requests.get("https://api.themoviedb.org/3/search/movie",
                                params=params)
    movie_search.raise_for_status()
    data = json.loads(movie_search.text)

    return render_template("select.html", movies=data)


@app.route("/find/<id>")
def find(id):
    movie_id = id
    params = {"api_key": config["MDB_API_KEY"], "language": "en-US"}
    movie_title_search = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}", params=params)
    movie_title_search.raise_for_status()
    data = json.loads(movie_title_search.text)
    img_id = data["poster_path"]
    add_movie_db = Movie(
        title=data["title"],
        year=data["release_date"][0:4],
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500/{img_id}",
    )
    db.session.add(add_movie_db)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
