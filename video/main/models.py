from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)

class Video(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)