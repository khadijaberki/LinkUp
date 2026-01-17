from django.contrib import admin
from django.urls import path
from authoo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('welcome/', views.welcome, name='welcome'),  # page après connexion
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('logout/', views.logout_view, name='logout'),
   
]
