from django.db import models

class ShortenedLink(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, )
    slug = models.CharField(max_length=10, null=False)
    url = models.URLField(max_length=200, null=False)