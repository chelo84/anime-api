import re
from datetime import datetime

import pymongo

from animeapi.util.list_util import ListUtil
from animeapi.util.param_util import ParamUtil
from animeapi.util.query_util import QueryUtil


class AnimeService:

    def __init__(self, animes_collection):
        self._animes_collection = animes_collection

    def find(self, req):
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

        return result

    def get_params(self, req):
        fields = ListUtil.filter_list(
            None,
            req.get_param('fields', default='').split(',')
        )
        fields_filter, order_by = self.get_fields_and_order_items(fields)

        params = {
            'offset': ParamUtil.get_int_param(req, 'offset', 0),
            'limit': ParamUtil.get_int_param(req, 'limit', 20),
            'name': req.get_param('name', default=None),
            'type': req.get_param('type', default=None),
            'fields': fields_filter,
            'order_by': order_by,
            'score_min': ParamUtil.get_float_param(req, 'score_min', 0.00),
            'score_max': ParamUtil.get_float_param(req, 'score_max', 10),
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

    def add_anime(self, req_json):
        new_anime = {'url': req_json.get('url'),
                     'image': req_json.get('image'),
                     'name': req_json.get('name'),
                     'type': req_json.get('type'),
                     'episodes': req_json.get('episodes'),
                     'status': req_json.get('status'),
                     'source': req_json.get('source'),
                     'genres': req_json.get('genres') if req_json.get('genres') and all(
                         type(genre) == str for genre in req_json.get('genres')) else [],
                     'synopsis': req_json.get('synopsis')}

        new_anime["created_at"] = datetime.now()
        result = self._animes_collection.insert_one(new_anime)
        id = result.inserted_id
        new_anime = self._animes_collection.find_one({'_id': id})

        return new_anime
