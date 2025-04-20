
import os
import sys
import logging
from datetime import datetime

from tmdb_client import TMDB_REST_API_Client
from discord_webhook import Discord_Webhook

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Movie_Announcer():

    def __init__(self):

        self.tmdb = TMDB_REST_API_Client(host="api.themoviedb.org", api_ver="3")

        status, output = self.get_genre_mapping()
        if not status:
            log.error(output)
            sys.exit(2)

        self.genre_map = output

        self.discord = Discord_Webhook(host="discord.com", base="api/webhooks")


    def notify_upcoming_movies(self):

        status, output = self.tmdb.get_movies_upcoming()
        if not status:
            log.error(output)
            os.exit(2)

        movies_candidate = []
        for movie in output:
            release_date = movie.get("release_date")
            release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
            today = datetime.today().date()
            if release_date <= today:
                continue
            movies_candidate.append(movie)

        sorted_movies = sorted(movies_candidate, key=lambda x: x["popularity"], reverse=True)

        for movie in sorted_movies[:5]:  # Limit to 5 to avoid spam
            embed = self.format_movie_embed(movie)
            status, response = self.discord.send_discord_message(content="🎬 Upcoming Movie!", embed=embed)
            if not status:
                log.error(f"Failed to send: {movie['title']}\n{response}")


    def format_movie_embed(self, movie):

        genre_ids = movie.get("genre_ids", [])
        genres = ", ".join([self.genre_map.get(gid, str(gid)) for gid in genre_ids])

        return {
            "title": movie["title"],
            "description": movie.get("overview", "")[:200] + "...",
            "color": 0x1abc9c,  # Teal
            "fields": [
                {
                  "name": "Release Date",
                  "value": movie.get("release_date", "N/A"),
                  "inline": True
                },
                {
                  "name": "Popularity",
                  "value": f"{int(movie.get('popularity', 0))} ⭐",
                  "inline": True
                },
                {
                  "name": "Genres",
                  "value": genres or "N/A",
                  "inline": False
                }
            ],
            "image": {
                "url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else ""
            }
        }


    def get_genre_mapping(self):

        status, output = self.tmdb.get_movie_genres()
        if not status:
            return False, "Could not fetch genre mapping."

        genres = {
            genre["id"]: genre["name"] for genre in output["genres"]
        }

        return True, genres


if __name__ == "__main__":

    notifier = Movie_Announcer()
    notifier.notify_upcoming_movies()
