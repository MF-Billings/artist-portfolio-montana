from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('artwork/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('biography/', views.biography, name='biography'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
]
