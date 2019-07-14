import falcon


class Check(object):
    def on_get(self, req, resp):
        resp.body = 'Everything is fine :)'
        resp.status = falcon.HTTP_OK
