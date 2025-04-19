import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def save_movie_detail(movie_id, data, ttl=600):
    key = f"movie:{movie_id}"
    r.set(key, json.dumps(data), ex=ttl)

def get_movie_detail(movie_id):
    key = f"movie:{movie_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_movie_credit_detail(credit_id, data, ttl=600):
    key = f"movie_credit:{credit_id}"
    r.set(key, json.dumps(data), ex=ttl)

def get_movie_credit_detail(credit_id):
    key = f"movie_credit:{credit_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

##############################################

def save_tv_detail(tv_id, data, ttl=600):
    key = f"tv:{tv_id}"
    r.set(key, json.dumps(data), ex=ttl)

def get_tv_detail(tv_id):
    key = f"tv:{tv_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

def save_tv_credit_detail(credit_id, data, ttl=600):
    key = f"tv_credit:{credit_id}"
    r.set(key, json.dumps(data), ex=ttl)

def get_tv_credit_detail(credit_id):
    key = f"tv_credit:{credit_id}"
    val = r.get(key)
    if val:
        return json.loads(val)
    return None

##############################################
