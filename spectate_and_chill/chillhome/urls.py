from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summoner/$', views.request_summoner, name='request_summoner'),
    url(r'^delay404/$', views.delay404, name='delay404'),
    url(r'^redis/$', views.redisTest, name='redisTest'),
    url(r'^recommendations/$', views.recommendations, name='recommendations'),
    url(r'^add/$', views.add_streamer, name='add_streamer'),
]