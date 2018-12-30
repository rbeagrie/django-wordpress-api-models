from common_models import common_models
import json
import urllib.request, urllib.parse, urllib.error
import rest_client

class WPModelManager(common_models.ModelManager):

    def __init__(self, model, finders, prefix):
        self.prefix = prefix
        super(WPModelManager,self).__init__(model, finders)

    def filter(self, **kw):
        return WPModelQuery(self, self.model, headers=self.headers, prefix=self.prefix).filter(**kw)

    def filter_custom(self, url):
        return WPModelQuery(self, self.model, headers=self.headers, prefix=self.prefix).filter_custom(url)

    def get(self, **kw):
        return WPModelQuery(self, self.model, headers=self.headers, prefix=self.prefix).get(**kw)

class WPModelQuery(common_models.ModelQuery):

    def __init__(self, manager, model, headers={}, prefix=False):
        self.manager = manager
        self.model = model
        self.args = {}
        self.headers = headers
        self.prefix = prefix
        if self.prefix:
            self._fragments = self._wp_fragments
        else:
            self._fragments = self._json_fragments

    def __getitem__(self, val):
        if isinstance( val, int ):
            index_params = {'number' : 1,
                            'offset' : val }
            url_query = urllib.parse.urlencode( index_params )

            response = rest_client.Client("").GET('%s?%s' % (self._find_query_path(), url_query), headers=self.headers)
            return self.model( next( self._fragments(response.content) ) )

        elif isinstance( val, slice ):
            if not val.step is None:
                raise IndexError("This API does not support stepping.")
            if val.start is None:
                index_params = {'number' : val.stop }
            elif val.stop is None:
                index_params = {'offset' : val.start }
            else:
                number = val.stop - val.start
                index_params = {'number' : number,
                            'offset' : val.start }

            url_query = urllib.parse.urlencode( index_params )

            response = rest_client.Client("").GET('%s?%s' % (self._find_query_path(), url_query), headers=self.headers)
            return [ self.model(fragment) for fragment in self._fragments(response.content) ]

        else:
            raise TypeError("Invalid argument type.")

    def _wp_fragments(self, response):
        for post_data in json.loads(response.read())[self.prefix]:
            yield json.dumps(post_data)
