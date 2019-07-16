import falcon


class PingResource(object):
    def on_get(self, req, resp):
        resp.body = 'Pong'
        resp.status = falcon.HTTP_OK
