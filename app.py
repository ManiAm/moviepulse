#!/usr/bin/env python3

# File: app.py
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com
# Description: Flask app serving moviePulse

import sys
import logging
from dotenv import load_dotenv
from tmdb_client import TMDB_REST_API_Client
from flask import Flask, render_template, Blueprint
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

@ns.route("/trending/tv")
class TrendingTV(Resource):
    def get(self):
        url = f"{tmdb.baseurl}/trending/tv/day"
        status, result = tmdb._TMDB_REST_API_Client__request("GET", url)
        if not status:
            return {"error": result}, 500
        return result

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

def _debug(tmdb):

    status, output = tmdb.discover_movies()
    if not status:
        log.error(output)
        sys.exit(2)

    status, output = tmdb.get_trending_movies()
    if not status:
        log.error(output)
        sys.exit(2)

    status, output = tmdb.get_movie_detail(movie_id=950387)
    if not status:
        log.error(output)
        sys.exit(2)

    status, output = tmdb.get_movie_credit(movie_id=950387)
    if not status:
        log.error(output)
        sys.exit(2)

#####################################

if __name__ == "__main__":

    app.run(debug=False, host="0.0.0.0", port=5000)
