
import os
import sys
import getpass
import json
import logging
import requests
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


    ########################
    ####### Trending #######
    ########################

    def get_trending_movies(self, language="en-US", time_window="day", max_pages=5):
        """
            time_window = day or week
        """

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
                return True, result_list

            page_num += 1


    def get_trending_tvs(self, language="en-US", time_window="day", max_pages=5):
        """
            time_window = day or week
        """

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
                return True, result_list

            page_num += 1


    ############################
    ####### Movie Detail #######
    ############################

    def get_movie_detail(self, movie_id, language="en-US"):

        cached = models_redis.get_movie_detail(movie_id)
        if cached:
            return True, cached

        url = f"{self.baseurl}/movie/{movie_id}"
        params = {"language": language}

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.save_movie_detail(movie_id, output)

        return True, output
 

    def get_movie_credit(self, movie_id, language="en-US"):

        cached = models_redis.get_movie_credit_detail(movie_id)
        if cached:
            return True, cached

        url = f"{self.baseurl}/movie/{movie_id}/credits"

        params = {
            "language": language
        }

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.save_movie_credit_detail(movie_id, output)

        return True, output


    def get_movie_video(self, movie_id, language="en-US"):

        url = f"{self.baseurl}/movie/{movie_id}/videos"

        params = {
            "language": language
        }

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        results = output.get("results", [])

        return True, results


    #########################
    ####### TV Detail #######
    #########################

    def get_tv_detail(self, tv_id, language="en-US"):

        cached = models_redis.get_tv_detail(tv_id)
        if cached:
            return True, cached

        url = f"{self.baseurl}/tv/{tv_id}"
        params = {"language": language}

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.save_tv_detail(tv_id, output)

        return True, output
 

    def get_tv_credit(self, tv_id, language="en-US"):

        cached = models_redis.get_tv_credit_detail(tv_id)
        if cached:
            return True, cached

        url = f"{self.baseurl}/tv/{tv_id}/credits"

        params = {
            "language": language
        }

        status, output = self.__request("GET", url, params=params)
        if not status:
            return False, output

        models_redis.save_tv_credit_detail(tv_id, output)

        return True, output


    ###############################
    ####### Discover Movies #######
    ###############################

    def discover_movies(self,
                        include_adult=False,
                        include_video=False,
                        language="en-US",
                        sort_by="popularity.desc",
                        region=None,
                        release_date_gte=None,
                        release_date_lte=None,
                        with_release_type=None,
                        without_genres=None,
                        vote_count_gte=None,
                        vote_count_lte=None,
                        max_pages=5):
        """
            Release	                Type
            Premiere	            1
            Theatrical (limited)	2
            Theatrical	            3
            Digital	                4
            Physical	            5
            TV	                    6
        """

        url = f"{self.baseurl}/discover/movie"

        page_num = 1
        result_list = []

        while True:

            params = {
                "page": page_num,
                "include_adult": include_adult,
                "include_video": include_video,
                "language": language,
                "sort_by": sort_by,
                "region": region,
                "release_date.gte": release_date_gte,
                "release_date.lte": release_date_lte,
                "with_release_type": with_release_type,
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
                return True, result_list

            page_num += 1


    def get_movies_popular(self):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc")


    def get_movies_now_playing(self):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc",
                                    with_release_type="2|3")


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


    def get_movies_top_rated(self):

        return self.discover_movies(include_adult=False,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="vote_average.desc",
                                    without_genres="99,10755",
                                    vote_count_gte=200)


    def get_movies_adults(self):

        return self.discover_movies(include_adult=True,
                                    include_video=False,
                                    language="en-US",
                                    max_pages=5,
                                    sort_by="popularity.desc")


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
                return True, result_list

            page_num += 1


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

    status, output = tmdb.get_trending_tvs()
    if not status:
        log.error(output)
        sys.exit(2)
