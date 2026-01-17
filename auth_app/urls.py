from django.contrib import admin
from django.urls import path
from authoo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('welcome/', views.welcome, name='welcome'),  # page après connexion
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
   path('add_friend_by_name/', views.add_friend_by_name, name='add_friend_by_name'),



    path('logout/', views.logout_view, name='logout'),
]

