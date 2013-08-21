import json_models
from meta_models import WPMetaModel

# Create your models here.
class Site(json_models.Model):
   id = json_models.IntField(path='ID')
   name = json_models.CharField(path='name')
   finders = { (id,): "https://public-api.wordpress.com/rest/v1/sites/%i" }

class Post(json_models.Model):
   __metaclass__ = WPMetaModel
   id = json_models.IntField(path='ID')
   # The wordpress API does not return the site_id for a post, but we need it as a key for the finder
   # so we'll just use a non-existant path... tldr: this is an ugly hack
   site_id = json_models.IntField(path='some.non.existant.path')
   title = json_models.CharField(path='title')
   url = json_models.CharField(path='URL')
   excerpt = json_models.CharField(path='excerpt')
   content = json_models.CharField(path='content')
   finders = { (site_id,): "https://public-api.wordpress.com/rest/v1/sites/%s/posts" }

   # The wordpress api returns a json object containing the keys 'found' and 'posts'. 
   # Setting the prefix makes it look like it only returns the contents of the 'posts' key.
   prefix = 'posts'

