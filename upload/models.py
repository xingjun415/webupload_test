from django.db import models

# Create your models here.
class FileInfo(models.Model):
    path = models.CharField(max_length=255)
