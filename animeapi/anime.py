import falcon
from bson import json_util


class Collection(object):
    ANIMES_PER_PAGE = 20

    def __init__(self, animes_collection):
        self._animes_collection = animes_collection

    def on_get(self, req, resp):
        try:
            page = int(req.get_param("page", default=1))
        except ValueError:
            msg = "Page parameter need to be an integer"
            raise falcon.HTTPBadRequest('Bad request', msg)

        print(page)
        result = json_util.dumps(list(self._animes_collection
                      .find({})
                      .skip((page - 1) * self.ANIMES_PER_PAGE)
                      .limit(self.ANIMES_PER_PAGE)))

        resp.body = result
        resp.status = falcon.HTTP_OK
