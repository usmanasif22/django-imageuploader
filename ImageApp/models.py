from django.db import models

# Create your models here.
class Image(models.Model):
    caption = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255)