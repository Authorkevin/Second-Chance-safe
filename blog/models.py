from django.db import models

# Create your models here.


class BlogPost(models.Model):
        headline = models.CharField(max_length=300)
        author = models.CharField(max_length=100)
        date = models.DateTimeField(auto_now_add=True)
        image = models.URLField(max_length=300)
        image_alt = models.CharField(max_length=300)
        slug = models.SlugField(max_length=50)
        article = models.TextField()

