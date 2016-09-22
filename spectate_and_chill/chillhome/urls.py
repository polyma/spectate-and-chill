from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summoner/$', views.request_summoner, name='request_summoner'),
    url(r'^delay404/$', views.delay404, name='delay404'),
]