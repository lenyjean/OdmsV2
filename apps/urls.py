from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_page, name='login'),
    path('home', homepage, name='homepage'),
]
