import os
import pickle

from flask import Flask, flash, redirect, render_template, request, session, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    STATIC_ROOT = app.static_folder
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    movies_by_popularity = (
        open(os.path.join(STATIC_ROOT, "popularity.txt"), "r").read().splitlines()
    )
    id2movie = pickle.load(open(os.path.join(STATIC_ROOT, "id2movies2.pkl"), "rb"))

    @app.route("/")
    def home():
        movies_short = movies_by_popularity[:100]
        movie_names = [id2movie[int(movie)] for movie in movies_short]
        return render_template(
            "/home.html", movies=movies_short, movie_names=movie_names
        )

    @app.route("/about")
    def about():
        return render_template("/about.html")

    @app.route("/search/<name>")
    def search(name):
        return redirect(url_for("home", name=name))

    @app.route("/recommend/<movie_id>", methods=("GET", "POST"))
    def recommend(movie_id):
        if request.method == "POST":
            return render_template("/recommend.html")
        
    return app
