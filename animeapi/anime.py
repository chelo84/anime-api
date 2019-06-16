import falcon
from bson import json_util

from animeapi.util.list_util import ListUtil


class Collection(object):

    def __init__(self, animes_collection):
        self._animes_collection = animes_collection

    def on_get(self, req, resp):
        try:
            offset = int(req.get_param('offset', default=1))
            limit = int(req.get_param('limit', default=20))
            genres = ListUtil.filter_list(
                None,
                req.get_param('genres', default='').split(',')
            )

            fields = ListUtil.filter_list(
                None,
                req.get_param('fields', default='').split(',')
            )

            result = list(
                self._animes_collection.find(({'genre': {'$in': genres} if len(genres) > 0 else None}))
                    .skip(offset)
                    .limit(limit)
            )

            animes = ListUtil.get_only_specific_fields(result, fields)

            resp.body = json_util.dumps(animes)
            resp.status = falcon.HTTP_OK

        except ValueError:
            msg = "Limit and offset parameters need to be a positive integer number"
            raise falcon.HTTPBadRequest('Bad request', msg)
        except KeyError as ex:
            msg = "The field {field} is not valid!".format(field=ex)
            raise falcon.HTTPBadRequest('Bad request', msg)
