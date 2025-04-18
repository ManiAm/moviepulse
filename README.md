## MoviePulse

My family loves watching movies and TV shows. But with so many titles to choose from — and new ones dropping every week — picking something everyone agrees on for movie night can turn into a mini-debate.

This inspired me to build something useful and fun: a web service that fetches trending movies and TV shows. It can show detailed info for each title, and offers a simple UI where my family can browse and vote on what to watch next. It's become our digital movie night assistant!

<img src="pics/movie_search.png" alt="segment" width="900">

The backend is built using Python Flask, which serves a RESTful web service exposing various endpoints to interact with movie and TV show data. It runs on my local Raspberry Pi cluster, specifically on the `artemis` node within my home network.

Since Flask’s built-in development server is not suitable for production use, I’ve deployed the backend using a Flask + Gunicorn + Nginx stack. This architecture ensures reliability, performance, and scalability for concurrent access.

All movie and TV data is fetched from The Movie Database (TMDb) - [API Reference](https://developer.themoviedb.org/reference/intro/getting-started). It provides a robust and well-documented REST API for accessing a wide range of metadata including trending content, credits, release information, etc.

To improve response time and reduce redundant calls, Flask leverages an in-memory Redis cache. Frequently accessed data is temporarily stored in Redis, allowing the system to serve cached results quickly rather than querying TMDb on every request. Redis is deployed in a Docker container to maintain state across reboots.

The project structure looks like:

    /moviepulse/
    ├── backend/
    │   ├── app.py
    │   ├── docker-compose.yml
    │   ├── models_redis.py
    │   ├── tmdb_client.py
    │   ├── requirements.txt
    │   └── .env  --> API token
    ├── frontend/
        ├── index.html
        ├── script.js
        ├── styles.css


------------------------------

adding a gif from dani playing with cozila and navigating

nginx config


- **Frontend**: HTML + CSS + JavaScript (fetch API)


i want to be able to use name to access the API: http://moviepulse --> should point to artemis

use cozyla to load the web page


Api service - send new movies to discord
