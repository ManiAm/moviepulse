## MoviePulse

My family loves watching movies and TV shows. But with so many titles to choose from — and new ones dropping every week — picking something everyone agrees on for movie night can turn into a mini-debate.

This inspired me to build something useful and fun: a web service that fetches trending movies and TV shows. It can show detailed info for each title, and offers a simple UI where my family can browse and vote on what to watch next. It's become our digital movie night assistant!

<img src="pics/movie_search.png" alt="segment" width="900">

The backend is built using Python Flask, which serves a RESTful web service exposing various endpoints to interact with movie and TV show data. It runs on my local Raspberry Pi cluster, specifically on the `artemis` node within my home network.

Since Flask’s built-in development server is not suitable for production use, I’ve deployed the backend using a Flask + Gunicorn + Nginx stack. This architecture ensures reliability, performance, and scalability for concurrent access.

All movie and TV data is fetched from The Movie Database (TMDb) - [API Reference](https://developer.themoviedb.org/reference/intro/getting-started). It provides a robust and well-documented REST API for accessing a wide range of metadata including trending content, credits, release information, etc.

To improve response time and reduce redundant calls, Flask leverages an in-memory Redis cache. Frequently accessed data is temporarily stored in Redis, allowing the system to serve cached results quickly rather than querying TMDb on every request. Redis is deployed in a Docker container to maintain state across reboots.

While Redis is ideal for caching transient data, persistent user-related information—such as interaction logs, preferences, watch history, and session metadata—is stored in a PostgreSQL database. SQLAlchemy serves as the ORM layer, providing a clean and Pythonic interface to interact with the database.

The project structure looks like:

    moviepulse/
        ├── app.py
        ├── tmdb_client.py
        ├── models_redis.py
        ├── models_sql.py
        ├── requirements.txt
        ├── docker-compose.yml
        ├── .env  ---> API token
        ├── templates/
        |   ├── index.html
        |   ├── movie_detail.html
        |   ├── tv_detail.html
        ├── static/
        │   ├── css
        │   └── js


------------------------------

nginx config

swagger doc - picture

add moviepulse.home into local DNS so that it redirects to artemis.home IP that is running NGINX

- Web-page: http://moviepulse.home/
- Swagger docs: http://moviepulse.home/api/docs
- API Base URL: http://moviepulse.home/api/v1/

------------------------------

Frontend: HTML + CSS + JavaScript (fetch API)

Sections in the page:

trending movies
trending tv shows
upcoming movies
popular movies
top-rated movies
horror movies
family animations

describe the difference between popular and top-rated from tmdb

for popular movies and top-rated movies user can filter the contents based on genre, regions, year, etc.

add a gif picture - adding multiple genre - year

use cozyla to load the web page

adding a gif from dani playing with cozila and navigating

to find age-appropriate content for your 6-year-old son like cartoons or family movies.

----------------------------

Api service - send new movies to discord

my wife is a big fan of marvel movies - send email when a marvel movie is released
