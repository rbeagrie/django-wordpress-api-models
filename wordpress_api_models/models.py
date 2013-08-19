import json_models

# Create your models here.
class Site(json_models.Model):
   id = json_models.IntField(path='ID')
   name = json_models.CharField(path='name')
   finders = { (id,): "https://public-api.wordpress.com/rest/v1/sites/%i" }

class Post(json_models.Model):
   id = json_models.IntField(path='posts.ID')
   # The wordpress API does not return the site_id for a post, but we need it as a key for the finder
   # so we'll just pretend the author ID is the same thing... tldr: this is an ugly hack
   site_id = json_models.IntField(path='posts.author.ID')
   title = json_models.CharField(path='posts.title')
   finders = { (site_id,): "https://public-api.wordpress.com/rest/v1/sites/%s/posts" }
