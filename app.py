#!/usr/bin/env python3

# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com
# Description: Flask app serving moviePulse

import os
import logging
from dotenv import load_dotenv
from tmdb_client import TMDB_REST_API_Client
from flask import Flask, render_template, Blueprint
from flask import request
from flask import send_from_directory
from flask_restx import Api, Resource
from sqlalchemy.exc import IntegrityError

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

# legacy browsers
@web_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@web_bp.route("/movie/<int:movie_id>")
def movie_detail_page(movie_id):
    return render_template("movie_detail.html", movie_id=movie_id)

@web_bp.route("/tv/<int:tv_id>")
def tv_detail_page(tv_id):
    return render_template("tv_detail.html", tv_id=tv_id)

@web_bp.route("/favorites")
def show_favorites():
    session = models_sql.Session()
    favorites = session.query(models_sql.Favorite).filter_by(username="guest").all()
    session.close()
    return render_template("favorites.html", favorites=favorites)

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
# API Base URL: http://artemis.home:5000/api/v1/

#####################################

@ns.route("/health")
class HealthCheck(Resource):
    def get(self):
        return {"status": "ok"}, 200

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

@ns.route("/genres")
class Genres(Resource):
    def get(self):
        status, result = tmdb.get_movie_genres()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/languages")
class Languages(Resource):
    def get(self):
        status, result = tmdb.get_languages()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/regions")
class Regions(Resource):
    def get(self):
        status, result = tmdb.get_countries()
        if not status:
            return {"error": result}, 500
        return result

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

@ns.route("/discover/upcoming")
class DiscoverUpcoming(Resource):
    def get(self):
        status, result = tmdb.get_movies_upcoming()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/popular")
class DiscoverPopular(Resource):
    def get(self):

        genres = request.args.get("with_genres")
        languages = request.args.get("language")
        regions = request.args.get("region")
        year = request.args.get("year")

        status, result = tmdb.get_movies_popular(with_genres=genres,
                                                 with_original_language=languages,
                                                 region=regions,
                                                 primary_release_year=year)
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/top_rated")
class DiscoverTopRated(Resource):
    def get(self):

        genres = request.args.get("with_genres")
        languages = request.args.get("language")
        regions = request.args.get("region")
        year = request.args.get("year")

        status, result = tmdb.get_movies_top_rated(with_genres=genres,
                                                   with_original_language=languages,
                                                   region=regions,
                                                   primary_release_year=year)
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/family_animation")
class DiscoverFamilyAnimation(Resource):
    def get(self):
        status, result = tmdb.get_movies_family_animation()
        if not status:
            return {"error": result}, 500
        return result

@ns.route("/discover/horror")
class DiscoverFamilyAnimation(Resource):
    def get(self):
        status, result = tmdb.get_movies_horror()
        if not status:
            return {"error": result}, 500
        return result

#####################################

@ns.route("/favorites")
class FavoriteList(Resource):

    def get(self):
        """Get list of favorite items for the guest user"""
        session = models_sql.Session()
        favs = session.query(models_sql.Favorite).filter_by(username="guest").all()
        session.close()
        return [ {"tmdb_id": f.tmdb_id, "media_type": f.media_type} for f in favs ]

    def post(self):
        """Add an item to favorites"""
        data = request.json
        session = models_sql.Session()
        fav = models_sql.Favorite(
            username="guest",
            tmdb_id=data["tmdb_id"],
            media_type=data["media_type"]
        )
        session.add(fav)

        try:
            session.commit()
            return {
                "success": True,
                "favorite": {
                    "tmdb_id": fav.tmdb_id,
                    "media_type": fav.media_type
                }
            }, 201
        except IntegrityError:
            session.rollback()
            return {"message": "Item already in favorites."}, 200
        finally:
            session.close()

    def delete(self):
        """Remove an item from favorites"""
        data = request.json
        session = models_sql.Session()
        fav = session.query(models_sql.Favorite).filter_by(
            username="guest",
            tmdb_id=data["tmdb_id"],
            media_type=data["media_type"]
        ).first()

        if fav:
            session.delete(fav)
            session.commit()
            result = {"success": True, "message": "Item removed from favorites."}
        else:
            result = {"success": False, "message": "Item not found in favorites."}

        session.close()
        return result, 200

#####################################

if __name__ == "__main__":

    models_sql.init_db()
    print("Database initialized.")

    app.run(debug=True, host="0.0.0.0", port=5000)
