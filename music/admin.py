from django.contrib import admin
from .models import Album, Song


class AlbumModel(admin.ModelAdmin):
    list_display = [
        'album_title', 'artist', 'genre', 'is_favorite'
    ]
    search_fields = [
        'album_title', 'artist', 'genre',
    ]


class SongModel(admin.ModelAdmin):
    list_display = [
        'song_title', 'album', 'is_favorite'
    ]
    search_fields = [
        'song_title'
    ]


admin.site.register(Album, AlbumModel)
admin.site.register(Song, SongModel)
