import falcon


class ParamUtil(object):
    @staticmethod
    def __get_param(req, param, default):
        return req.get_param(param, default=default)

    @staticmethod
    def get_int_param(req, param, default):
        try:
            return int(ParamUtil.__get_param(req, param, default))
        except ValueError as ex:
            print(getattr(ex, 'message', repr(ex)))
            raise falcon.HTTPBadRequest('Wrong parameter', 'Parameter ' + param + ' need to be an integer.')

    @staticmethod
    def get_float_param(req, param, default):
        try:
            return float(ParamUtil.__get_param(req, param, default))
        except ValueError as ex:
            print(getattr(ex, 'message', repr(ex)))
            raise falcon.HTTPBadRequest('Wrong parameter', 'Parameter ' + param + ' need to be a float number.')
