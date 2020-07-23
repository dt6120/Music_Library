from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Album, Song
from .forms import UserForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AlbumSerializer


# Create your views here.
class AlbumIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'music/album_index.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.filter().order_by('album_title')


class AlbumDetailView(LoginRequiredMixin, generic.DeleteView):
    model = Album
    template_name = 'music/album_detail.html'
    # context_object_name = 'album_detail'


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    template_name = 'music/album_form.html'
    fields = [
        'artist', 'album_title', 'genre', 'album_logo', 'is_favorite'
    ]

    # If the model requires User field that has to be fetched automatically,
    # then use the form_valid() function to manually set the user as request.user

    # If you want to redirect to a specific page other than the DetailView as specified in the
    # get_absolute_url() function, you can override that by changing success_url parameter


class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('music:album_index')


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    template_name = 'music/album_form.html'
    fields = [
        'artist', 'album_title', 'genre', 'album_logo', 'is_favorite'
    ]


class SongListView(LoginRequiredMixin, generic.ListView):
    model = Song
    template_name = 'music/song_index.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.order_by('song_title')


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'music/signup_user.html'
    success_url = reverse_lazy('music:album_index')

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('music:album_index')
            except IntegrityError:
                return render(request, self.template_name, {
                    'form': self.form_class,
                    'error': 'Username already exists.'
                })
        else:
            return render(request, self.template_name, {
                'form': self.form_class,
                'error': 'Passwords didn\'t match..'
            })


class LoginView(CreateView):
    form_class = AuthenticationForm
    template_name = 'music/login_user.html'
    success_url = reverse_lazy('music:album_index')

    def post(self, request, *args, **kwargs):
        user_exists = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user_exists:
            login(request, user_exists)
            return redirect('music:album_index')
        else:
            return render(request, self.template_name, {
                'form': self.form_class,
                'error': 'User credentials invalid.'
            })


def toggle_fav_album(request, pk):
    album = get_object_or_404(Album, pk=pk)
    album.is_favorite = not album.is_favorite
    album.save()
    return redirect('music:album_index')


def toggle_fav_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    song.is_favorite = not song.is_favorite
    song.save()
    album_id = Album.objects.get(song=song).id
    return redirect('music:album_detail', album_id)


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'music/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                login(request, user)
                return redirect('music:album_index')
            except IntegrityError:
                return render(request, 'music/signup_user.html', {'form':UserCreationForm(), 'error': 'Username already exists.'})
        else:
            return render(request, 'music/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'Passwords didn\'t match.'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'music/login_user.html', {'form': AuthenticationForm()})
    else:
        user_exists = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user_exists:
            login(request, user_exists)
            return redirect('music:album_index')
        else:
            return render(request, 'music/login_user.html', {'form': UserCreationForm(), 'error': 'User credentials invalid.'})


def logout_user(request):
    logout(request)
    return redirect('login_user')


class AlbumAPI(APIView):
    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass
