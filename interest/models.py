from django.db import models

# Create your models here.

class Interest(models.Model):
    title = models.CharField('가수', max_length=50)
    artist = models.CharField('제목', max_length=50)

    def __str__(self):
        return self.artist