import re

import falcon
import pymongo
from bson import json_util

from animeapi.util.list_util import ListUtil
from animeapi.util.query_util import QueryUtil


class Anime(object):

    def __init__(self, animes_collection):
        self._animes_collection = animes_collection

    def on_get(self, req, resp):
        params = self.get_params(req)

        params['order_by'] = params['order_by'] if len(params['order_by']) > 0 else [["_id", pymongo.ASCENDING]]

        query = {}

        if len(params['genres']) > 0:
            query['genres'] = QueryUtil.query_all(params['genres'])
        if len(params['producers']) > 0:
            query['producers'] = QueryUtil.query_in(params['producers'])
        if len(params['studios']) > 0:
            query['studios'] = QueryUtil.query_in(params['studios'])
        if len(params['source']) > 0:
            query['source'] = QueryUtil.query_in(params['source'])
        if params['name']:
            query['name'] = QueryUtil.query_regex(params['name'])

        query['score'] = QueryUtil.query_between(params['score_min'], params['score_max'])

        result = list(
            self._animes_collection
                .find(query,
                      params['fields'])
                .skip(params['offset'])
                .limit(params['limit'])
                .sort(params['order_by'])
        )

        resp.body = json_util.dumps(result)
        resp.status = falcon.HTTP_OK

    def get_params(self, req):
        try:
            fields = ListUtil.filter_list(
                None,
                req.get_param('fields', default='').split(',')
            )
            fields_filter, order_by = self.get_fields_and_order_items(fields)

            params = {
                'offset': int(req.get_param('offset', default=0)),
                'limit': int(req.get_param('limit', default=20)), 'name': req.get_param('name', default=None),
                'type': req.get_param('type', default=None),
                'fields': fields_filter,
                'order_by': order_by,
                'score_min': float(req.get_param('score_min', default=0.00)),
                'score_max': float(req.get_param('score_max', default=10)),
                'genres': ListUtil.filter_list(
                    None,
                    req.get_param('genres', default='').split(',')
                ),
                'producers': ListUtil.filter_list(
                    None,
                    req.get_param('producers', default='').split(',')
                ),
                'studios': ListUtil.filter_list(
                    None,
                    req.get_param('studios', default='').split(',')
                ),
                'source': ListUtil.filter_list(
                    None,
                    req.get_param('sources', default='').split(',')
                )
            }

            return params

        except ValueError as ex:
            raise falcon.HTTPBadRequest('Bad request', ex)

    def get_fields_and_order_items(self, fields):
        order_by = []
        fields_filter = (None, {})[len(fields) > 0]
        for field in fields:
            first_character = field[0]
            if re.match('\+|-', first_character):
                field = field.replace(first_character, '', 1).strip()
                order = pymongo.ASCENDING if first_character == '+' else pymongo.DESCENDING
                order_by.append([field, order])

            fields_filter[field] = 1
        return fields_filter, order_by
