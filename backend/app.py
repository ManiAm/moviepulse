#!/usr/bin/env python3

# File: app.py
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com
# Description: Flask app serving moviePulse

import sys
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from tmdb_client import TMDB_REST_API_Client

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# Load TMDB API token from environment
load_dotenv()

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

# Create TMDB API client
tmdb = TMDB_REST_API_Client(host="api.themoviedb.org", api_ver="3")

_debug(tmdb)

app = Flask(__name__)

@app.route("/api/trending/movies", methods=["GET"])
def trending_movies():
    status, result = tmdb.get_trending_movies()
    if not status:
        return jsonify({"error": result}), 500
    return jsonify(result)

@app.route("/api/movie/<int:movie_id>", methods=["GET"])
def movie_detail(movie_id):
    status, result = tmdb.get_movie_detail(movie_id)
    if not status:
        return jsonify({"error": result}), 500
    return jsonify(result)

@app.route("/api/movie/<int:movie_id>/credits", methods=["GET"])
def movie_credits(movie_id):
    status, result = tmdb.get_movie_credit(movie_id)
    if not status:
        return jsonify({"error": result}), 500
    return jsonify(result)

@app.route("/api/trending/tv", methods=["GET"])
def trending_tv():
    url = f"{tmdb.baseurl}/trending/tv/day"
    status, result = tmdb._TMDB_REST_API_Client__request("GET", url)
    if not status:
        return jsonify({"error": result}), 500
    return jsonify(result)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=5000)
