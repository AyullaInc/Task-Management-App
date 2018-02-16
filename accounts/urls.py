from django.conf.urls import url,include
from django.contrib import admin
from .views import home,team_signup,login

urlpatterns = [
    url(r'^$',home),
    url(r'^create-team$',team_signup),
    url(r'^login$',login),
]