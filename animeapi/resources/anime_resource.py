import falcon
from bson import json_util
from falcon.media.validators import jsonschema

from animeapi.schemas import load_schema
from animeapi.services.anime_service import AnimeService


class AnimeResource:

    def __init__(self, animes_collection):
        self._anime_service = AnimeService(animes_collection)

    def on_get(self, req, resp):
        result = self._anime_service.find(req)

        pretty = req.get_param('pretty', default='False').lower() == 'true'
        resp.body = json_util.dumps(result, indent=(4 if pretty else None))
        resp.status = falcon.HTTP_OK

    @jsonschema.validate(load_schema('new_anime'))
    def on_post(self, req, resp):
        req_json = req.media

        new_anime = self._anime_service.add_anime(req_json)

        resp.body = json_util.dumps(new_anime)
        resp.status = falcon.HTTP_CREATED
