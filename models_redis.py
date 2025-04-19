import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_movie_certification():
    key = "movie_cert"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_movie_certification(data, ttl=600):
    key = "movie_cert"
    r.set(key, json.dumps(data), ex=ttl)

def get_countries():
    key = "countries"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_countries(data, ttl=600):
    key = "countries"
    r.set(key, json.dumps(data), ex=ttl)

def get_languages():
    key = "language"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_languages(data, ttl=600):
    key = "language"
    r.set(key, json.dumps(data), ex=ttl)

def get_movie_genres():
    key = "movie_genres"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_movie_genres(data, ttl=600):
    key = "movie_genres"
    r.set(key, json.dumps(data), ex=ttl)

##############################################

def get_movie_detail(movie_id):
    key = f"movie:{movie_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_movie_detail(movie_id, data, ttl=600):
    key = f"movie:{movie_id}"
    r.set(key, json.dumps(data), ex=ttl)

def get_movie_credit_detail(credit_id):
    key = f"movie_credit:{credit_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_movie_credit_detail(credit_id, data, ttl=600):
    key = f"movie_credit:{credit_id}"
    r.set(key, json.dumps(data), ex=ttl)

##############################################

def get_tv_detail(tv_id):
    key = f"tv:{tv_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_tv_detail(tv_id, data, ttl=600):
    key = f"tv:{tv_id}"
    r.set(key, json.dumps(data), ex=ttl)

def get_tv_credit_detail(credit_id):
    key = f"tv_credit:{credit_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_tv_credit_detail(credit_id, data, ttl=600):
    key = f"tv_credit:{credit_id}"
    r.set(key, json.dumps(data), ex=ttl)

##############################################
