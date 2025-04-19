#!/usr/bin/env python3

# File: app.py
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com
# Description: Flask app serving moviePulse

import logging
from dotenv import load_dotenv
from tmdb_client import TMDB_REST_API_Client
from flask import Flask, render_template, Blueprint
from flask import request
from flask_restx import Api, Resource

import models_sql

#####################################

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

#####################################

load_dotenv()

app = Flask(__name__)
tmdb = TMDB_REST_API_Client(host="api.themoviedb.org", api_ver="3")

#####################################

# Create a blueprint for the web routes
web_bp = Blueprint("web", __name__, template_folder="templates")

@web_bp.route("/")
def home():
    return render_template("index.html")

@web_bp.route("/movie/<int:movie_id>")
def movie_detail_page(movie_id):
    return render_template("movie_detail.html", movie_id=movie_id)

@web_bp.route("/tv/<int:tv_id>")
def tv_detail_page(tv_id):
    return render_template("tv_detail.html", tv_id=tv_id)

# Register blueprint for web routes
app.register_blueprint(web_bp)

# Web-page: http://artemis.home:5000/

#####################################

# Initialize Flask-RESTX API
api = Api(app,
          version="1.0",
          title="MoviePulse REST API",
          description="MoviePulse REST API",
          prefix="/api",
          doc="/api/docs")

# Define API Namespace
ns = api.namespace("v1", description="")

# Swagger docs: http://artemis.home:5000/api/docs
# Base URL: http://artemis.home:5000/api/v1/

#####################################

@ns.route("/trending/movies")
class TrendingMovies(Resource):
    def get(self):
        status, result = tmdb.get_trending_movies()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/movie/<int:movie_id>")
class MovieDetail(Resource):
    def get(self, movie_id):
        status, result = tmdb.get_movie_detail(movie_id)
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/movie/<int:movie_id>/credits")
class MovieCredits(Resource):
    def get(self, movie_id):
        status, result = tmdb.get_movie_credit(movie_id)
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/movie/<int:movie_id>/videos")
class MovieVideos(Resource):
    def get(self, movie_id):
        status, result = tmdb.get_movie_video(movie_id)
        if not status:
            return {"error": result}, 500
        return result

#####################################

@ns.route("/trending/tv")
class TrendingTV(Resource):
    def get(self):
        status, result = tmdb.get_trending_tvs()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/tv/<int:tv_id>")
class TvDetail(Resource):
    def get(self, tv_id):
        status, result = tmdb.get_tv_detail(tv_id)
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/tv/<int:tv_id>/credits")
class TvCredits(Resource):
    def get(self, tv_id):
        status, result = tmdb.get_tv_credit(tv_id)
        if not status:
            return {"error": result}, 500
        return result

#####################################

@ns.route("/discover/popular")
class DiscoverPopular(Resource):
    def get(self):
        status, result = tmdb.get_movies_popular()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/upcoming")
class DiscoverUpcoming(Resource):
    def get(self):
        status, result = tmdb.get_movies_upcoming()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/top_rated")
class DiscoverTopRated(Resource):
    def get(self):
        status, result = tmdb.get_movies_top_rated()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/adults")
class DiscoverAdults(Resource):
    def get(self):
        status, result = tmdb.get_movies_adults()
        if not status:
            return {"error": result}, 500
        return result

#####################################

@ns.route("/search")
class Search(Resource):
    def get(self):
        query = request.args.get("query")
        if not query:
            return {"error": "Missing search query"}, 400
        status, result = tmdb.search(query)
        if not status:
            return {"error": result}, 500
        return result

#####################################

@ns.route("/health")
class HealthCheck(Resource):
    def get(self):
        return {"status": "ok"}, 200

#####################################

        # session = models_sql.Session()

        # # Check if movie_id is already cached in `movie_detail` table
        # cached = session.query(models_sql.MovieDetail).filter_by(movie_id=movie_id).first()
        # if cached:
        #     return True, cached.data


        # Save result in DB
        # new_entry = models_sql.MovieDetail(movie_id=movie_id, data=output)
        # session.add(new_entry)
        # session.commit()

#####################################

if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=5000)
