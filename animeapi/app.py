import falcon
import pymongo
import animeapi.anime as anime

MONGO_SERVER = 'localhost'
MONGO_PORT = 27017
MONGO_ANIMES_COLLECTION = 'animes'
MONGO_DB = 'animeDB'


def create_app(collection):
    api = falcon.API()
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
