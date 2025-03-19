from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('increment-score/', views.increment_score, name='increment_score'),
    path('get-leaderboard/', views.get_leaderboard, name='get_leaderboard'),
    path('', views.home, name='home'),
]
