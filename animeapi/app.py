import os
import sys

import falcon
import pymongo
from falcon.http_status import HTTPStatus

import animeapi.resources.anime_resource as anime_resource
import animeapi.resources.home_resource as home_resource
import animeapi.resources.ping_resource as ping_resource

MONGO_SERVER = (os.getenv('MONGO_HOST') or 'localhost')
MONGO_USER = (os.getenv('MONGO_USER') or None)
MONGO_PASS = (os.getenv('MONGO_PASS') or None)
MONGO_PORT = int(os.getenv('MONGO_PORT') or 27017)
MONGO_ANIMES_COLLECTION = 'animes'
MONGO_DB = (os.getenv('MONGO_DB') or 'animeDB')

print('Mongo server: ' + MONGO_SERVER +
      '\nMongo port: ' + str(MONGO_PORT) +
      '\nMongo DB: ' + MONGO_DB +
      '\nMongo collection: ' + MONGO_ANIMES_COLLECTION)
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
    api.add_route('/', home_resource.HomeResource())
    api.add_route('/ping', ping_resource.PingResource())
    api.add_route('/animes', anime_resource.AnimeResource(collection))
    return api


def get_app():
    connection = pymongo.MongoClient(
        MONGO_SERVER,
        MONGO_PORT
    )
    db = connection[MONGO_DB]
    if MONGO_USER and MONGO_PASS:
        db.authenticate(MONGO_USER, MONGO_PASS)

    animes_collection = db[MONGO_ANIMES_COLLECTION]

    return create_app(animes_collection)


api = get_app()
