from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Album(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.CharField(max_length=20)
    album_title = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:album_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=20)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title + ' - ' + self.album.artist
