from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.AlbumIndexView.as_view(), name='album_index'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('album/create', views.AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),
    path('album/<int:pk>/update/', views.AlbumUpdateView.as_view(), name='album_update'),
    path('songs', views.SongListView.as_view(), name='song_index'),
    path('album/<int:pk>/favorite/', views.toggle_fav_album, name='toggle_fav_album'),
    path('song/<int:pk>/favorite/', views.toggle_fav_song, name='toggle_fav_song'),
    # path('song/<int:pk>/favorite', views. , name='favorite_song'),
    # path('song/<int:pk>/edit', views. , name='edit_song'),
    # path('song/<int:pk>/delete', views. , name='delete_song'),
]
