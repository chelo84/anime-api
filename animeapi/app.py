import os
import sys

import falcon
import pymongo
from falcon.http_status import HTTPStatus

import animeapi.anime as anime
from animeapi.local_settings import environment

if environment == 'prd':
    MONGO_SERVER = '{user}:{password}@{host}'.format(user=os.environ['MONGO_USER'], password=os.environ['MONGO_PASS'],
                                                     host=os.environ['MONGO_HOST'])
    MONGO_PORT = int(os.environ['MONGO_PORT'])
    MONGO_ANIMES_COLLECTION = 'animes'
    MONGO_DB = os.environ['MONGO_DB']
else:
    MONGO_SERVER = '{host}'.format(host='localhost')
    MONGO_PORT = 27017
    MONGO_ANIMES_COLLECTION = 'animes'
    MONGO_DB = 'animeDB'

print('Mongo server: ' + MONGO_SERVER +
      'Mongo port: ' + MONGO_PORT +
      'Mongo DB: ' + MONGO_DB +
      'Mongo collection: ' + MONGO_ANIMES_COLLECTION)
sys.stdout.flush()


class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')


def create_app(collection):
    api = falcon.API(middleware=[HandleCORS()])
    api.add_route('/animes', anime.Collection(collection))
    # api.add_route('/anime/{page:int}', anime.Collection(collection))
    return api


def get_app():
    connection = pymongo.MongoClient(
        MONGO_SERVER,
        MONGO_PORT
    )
    db = connection[MONGO_DB]
    animes_collection = db[MONGO_ANIMES_COLLECTION]

    return create_app(animes_collection)


api = get_app()
