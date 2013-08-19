from common_models import common_models
import json

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

    def _wp_fragments(self, response):
        for post_data in json.loads(response.read())[self.prefix]:
            yield json.dumps(post_data)
