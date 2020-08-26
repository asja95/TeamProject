from django.db import models

# Create your models here.

class Keywords(models.Model):
    song = models.CharField('제목', max_length=50)
    album = models.CharField('앨범', max_length=50)
    artist = models.CharField('가수', max_length=20)
    lyrics = models.TextField('가사', max_length=5000)
    release = models.CharField('발매날짜', max_length=10)
    genre = models.CharField('장르', max_length=20)
    image = models.CharField('포스터', max_length=20)

    def __str__(self):
        return self.song


class Theme(models.Model):
    song = models.CharField('제목', max_length=50)
    album = models.CharField('앨범', max_length=50)
    artist = models.CharField('가수', max_length=20)
    lyrics = models.TextField('가사', max_length=5000)
    release = models.CharField('발매날짜', max_length=10)
    genre = models.CharField('장르', max_length=20)
    type = models.CharField('테마', max_length=10)

    def __str__(self):
        return self.type


class Chart(models.Model):
    song = models.CharField('제목', max_length=50)
    artist = models.CharField('가수', max_length=20)
    release = models.CharField('발매날짜', max_length=10)
    genre = models.CharField('장르', max_length=10)

    def __str__(self):
        return self.genre


class Name(models.Model):
    number = models.CharField('번호', max_length=10)
    name = models.CharField('장르', max_length=20)

    def __str__(self):
        return self.name
