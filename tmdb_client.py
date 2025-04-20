
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com
# Description: REST client for TMDb

import os
import sys
import getpass
import json
import logging
import requests
import inspect
from datetime import datetime
from dateutil.relativedelta import relativedelta

import models_redis

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

class TMDB_REST_API_Client():

    def __init__(self,
                 host=None,
                 port=None,
                 api_ver=None,
                 base=None,
                 user=getpass.getuser()):

        if not host:
            log.error("host is missing!")
            sys.exit(2)

        if not TMDB_REST_API_Client.__with_http_prefix(host):
            host_address = f'https://{host}'
        else:
            host_address = host

        if port:
            host_address += f':{port}'

        self.baseurl = f'{host_address}'

        if api_ver:
            self.baseurl += f'/{api_ver}'

        if base:
            self.baseurl += f'/{base}'

        self.user = user

        self.headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        }

        access_token = os.getenv('TMDB_API_TOKEN', None)
        if access_token:
            self.headers['Authorization'] = f'Bearer {access_token}'


    #######################
    ####### Configs #######
    #######################

    def get_movie_certification(self):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/certification/movie/list"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output


    def get_countries(self):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/configuration/countries"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output


    def get_languages(self):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/configuration/languages"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output


    def get_movie_genres(self):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/genre/movie/list"

        status, output = self.__request("GET", url)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output


    ########################
    ####### Trending #######
    ########################

    def get_trending_movies(self, language="en-US", time_window="day", max_pages=5):
        """
            time_window = day or week
        """

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/trending/movie/{time_window}"

        page_num = 1
        result_list = []

        while True:

            params = {
                "page": page_num,
                "language": language
            }

            status, output = self.__request("GET", url, params=params)
            if not status:
                return False, output

            results = output.get("results", [])
            result_list.extend(results)

            total_pages = output.get("total_pages", 0)

            if page_num >= min(max_pages, total_pages):
                break

            page_num += 1

        models_redis.set_to_cache(frame, result_list)

        return True, result_list


    def get_trending_tvs(self, language="en-US", time_window="day", max_pages=5):
        """
            time_window = day or week
        """

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/trending/tv/{time_window}"

        page_num = 1
        result_list = []

        while True:

            params = {
                "page": page_num,
                "language": language
            }

            status, output = self.__request("GET", url, params=params)
            if not status:
                return False, output

            results = output.get("results", [])
            result_list.extend(results)

            total_pages = output.get("total_pages", 0)

            if page_num >= min(max_pages, total_pages):
                break

            page_num += 1

        models_redis.set_to_cache(frame, result_list)

        return True, result_list


    ############################
    ####### Movie Detail #######
    ############################

    def get_movie_detail(self, movie_id, language="en-US"):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/movie/{movie_id}"
        params = {"language": language}

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output
 

    def get_movie_credit(self, movie_id, language="en-US"):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/movie/{movie_id}/credits"

        params = {
            "language": language
        }

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output


    def get_movie_video(self, movie_id, language="en-US"):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/movie/{movie_id}/videos"

        params = {
            "language": language
        }

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        results = output.get("results", [])

        models_redis.set_to_cache(frame, results)

        return True, results


    #########################
    ####### TV Detail #######
    #########################

    def get_tv_detail(self, tv_id, language="en-US"):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/tv/{tv_id}"
        params = {"language": language}

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output
 

    def get_tv_credit(self, tv_id, language="en-US"):

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/tv/{tv_id}/credits"

        params = {
            "language": language
        }

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.set_to_cache(frame, output)

        return True, output


    ###############################
    ####### Discover Movies #######
    ###############################

    def discover_movies(self,
                        include_adult=False,
                        include_video=False,
                        language="en-US",
                        with_original_language=None,
                        sort_by="popularity.desc",
                        region=None,
                        certification=None,
                        primary_release_year=None,
                        release_date_gte=None,
                        release_date_lte=None,
                        with_release_type=None,
                        with_genres=None,
                        without_genres=None,
                        vote_count_gte=None,
                        vote_count_lte=None,
                        max_pages=5):
        """
            | US Certification | Meaning                                                                                                                                                |
            |------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
            | G                | All ages admitted. There is no content that would be objectionable to most parents.                                                                    |
            | PG               | Some material may not be suitable for children under 10.                                                                                               |
            | PG-13            | Some material may be inappropriate for children under 13.                                                                                              |
            |                  | Films may contain sexual content, partial nudity, some strong language, humor, mature themes, political themes, terror and/or intense action violence. |
            | R                | Under 17 requires accompanying parent or adult guardian 21 or older.                                                                                   |
            |                  | May contain strong profanity, graphic sexuality, nudity, strong violence, horror, gore, and strong drug use.                                           |
            | NC-17            | These films contain excessive graphic violence, intense or explicit sex, depraved, abhorrent behavior, explicit drug abuse, strong language,           |
            |                  | explicit nudity, or any other elements which, at present, most parents would consider too strong and therefore off-limits for viewing by their children and teens. |
            | NR               | No rating information.                                                                                                                                 |

            | Release Type         | Type ID |
            |----------------------|---------|
            | Premiere             | 1       |
            | Theatrical (limited) | 2       |
            | Theatrical           | 3       |
            | Digital              | 4       |
            | Physical             | 5       |
            | TV                   | 6       |

            | Genre ID | Genre Name        |
            |----------|-------------------|
            | 28       | Action            |
            | 12       | Adventure         |
            | 16       | Animation         |
            | 35       | Comedy            |
            | 80       | Crime             |
            | 99       | Documentary       |
            | 18       | Drama             |
            | 10751    | Family            |
            | 14       | Fantasy           |
            | 36       | History           |
            | 27       | Horror            |
            | 10402    | Music             |
            | 9648     | Mystery           |
            | 10749    | Romance           |
            | 878      | Science Fiction   |
            | 10770    | TV Movie          |
            | 53       | Thriller          |
            | 10752    | War               |
            | 37       | Western           |
        """

        frame = inspect.currentframe()
        cached = models_redis.get_from_cache(frame)
        if cached:
            return True, cached

        url = f"{self.baseurl}/discover/movie"

        page_num = 1
        result_list = []

        while True:

            params = {
                "page": page_num,
                "include_adult": include_adult,
                "include_video": include_video,
                "language": language,
                "with_original_language": with_original_language,
                "sort_by": sort_by,
                "region": region,
                "certification": certification,
                "primary_release_year": primary_release_year,
                "release_date.gte": release_date_gte,
                "release_date.lte": release_date_lte,
                "with_release_type": with_release_type,
                "with_genres": with_genres,
                "without_genres": without_genres,
                "vote_count.gte": vote_count_gte,
                "vote_count.lte": vote_count_lte
            }

            status, output = self.__request("GET", url, params=params)
            if not status:
                return False, output

            results = output.get("results", [])
            result_list.extend(results)

            total_pages = output.get("total_pages", 0)

            if page_num >= min(max_pages, total_pages):
                break

            page_num += 1

        models_redis.set_to_cache(frame, result_list)

        return True, result_list


    #####################################
    ####### Discover-based Movies #######
    #####################################

    def get_movies_upcoming(self):

        today = datetime.today()
        today_str = today.strftime("%Y-%m-%d")

        # Add 3 months
        three_months_later = today + relativedelta(months=3)
        three_months_str = three_months_later.strftime("%Y-%m-%d")

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc",
                                    region="US",
                                    with_release_type="2|3",
                                    release_date_gte=today_str,
                                    release_date_lte=three_months_str)


    def get_movies_popular(self, with_genres=None, with_original_language=None, region=None, primary_release_year=None):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc",
                                    with_genres=with_genres,
                                    with_original_language=with_original_language,
                                    region=region,
                                    primary_release_year=primary_release_year)


    def get_movies_top_rated(self, with_genres=None, with_original_language=None, region=None, primary_release_year=None):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="vote_average.desc",
                                    vote_count_gte=200,
                                    without_genres="99,10755",
                                    with_genres=with_genres,
                                    with_original_language=with_original_language,
                                    region=region,
                                    primary_release_year=primary_release_year)


    def get_movies_family_animation(self):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc",
                                    with_genres="16,10751")


    def get_movies_horror(self):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc",
                                    with_genres="27")

    ######################
    ####### Search #######
    ######################

    def search(self, query, max_pages=5):

        url = f"{self.baseurl}/search/multi"

        page_num = 1
        result_list = []

        while True:

            params = {
                "query": query,
                "language": "en-US",
                "include_adult": False
            }

            status, output = self.__request("GET", url, params=params)
            if not status:
                return False, output

            results = output.get("results", [])
            result_list.extend(results)

            total_pages = output.get("total_pages", 0)

            if page_num >= min(max_pages, total_pages):
                break

            page_num += 1

        return True, result_list


    ##############################
    ####### Helper Methods #######
    ##############################

    @staticmethod
    def __with_http_prefix(host):

        if host.startswith("http://"):
            return True

        if host.startswith("https://"):
            return True

        return False


    def __request(self, method, url, timeout=10, verify=True, stream=False, decode=True, **kwargs):

        try:
            response = requests.request(method,
                                        url,
                                        headers=self.headers,
                                        timeout=timeout,
                                        verify=verify,
                                        stream=stream,
                                        **kwargs)
        except Exception as E:
            return False, str(E)

        try:
            response.raise_for_status()
        except Exception as E:
            return False, f'Return code={response.status_code}, {E}\n{response.text}'

        if stream:
            return True, response

        if not decode:
            return True, response.content

        try:
            content_decoded = response.content.decode('utf-8')
            if not content_decoded:
                return True, {}

            data_dict = json.loads(content_decoded)
        except Exception as E:
            return False, f'Error while decoding content: {E}'

        return True, data_dict


if __name__ == "__main__":

    tmdb = TMDB_REST_API_Client(host="api.themoviedb.org", api_ver="3")

    status, output = tmdb.get_countries()
    status, output = tmdb.get_languages()

    bla = 0
