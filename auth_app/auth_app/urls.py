from django.contrib import admin
from django.urls import path
from authoo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('welcome/', views.welcome),  # page après connexion
]

