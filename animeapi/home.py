import falcon


class Home(object):
    def on_get(self, req, resp):
        resp.body = '<div style="display: flex;align-items: center;flex-direction: column;">' \
                        '<h3>' \
                            'No princess in here :(' \
                        '</h3>' \
                        '<h3>' \
                            'Try another castle' \
                        '</h3>' \
                    '</div>'
        resp.content_type = falcon.MEDIA_HTML
        resp.status = falcon.HTTP_OK
