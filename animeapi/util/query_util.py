import re


class QueryUtil(object):
    @staticmethod
    def query_in(query_list):
        return {
            '$in': list(
                map(
                    lambda query_param: re.compile('^' + query_param + '$', re.IGNORECASE),
                    query_list
                )
            )
        }

    @staticmethod
    def query_all(query_list):
        return {
            '$all': list(
                map(
                    lambda query_param: re.compile('^' + query_param + '$', re.IGNORECASE),
                    query_list
                )
            )
        }

    @staticmethod
    def query_regex(query_param):
        return re.compile(query_param, re.IGNORECASE)

    @staticmethod
    def query_gt(query_param):
        return {
            '$gt': query_param
        }

    @staticmethod
    def query_lt(query_param):
        return {
            '$lt': query_param
        }

    @staticmethod
    def query_between(query_param_min, query_param_max):
        return {
            '$gte': query_param_min,
            '$lte': query_param_max
        }
