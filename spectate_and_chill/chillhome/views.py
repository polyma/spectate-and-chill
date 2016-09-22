from django.shortcuts import render
from django.http import HttpResponse, Http404

import json
import time
import redis


# Create your views here.
def index(request):
    #return HttpResponse("You made it!")
    return render(request, 'chillhome/index.html')


def request_summoner(request):
    return HttpResponse()

def delay404(request):
    time.sleep(5)
    raise Http404()

def redisTest(request):
    r = redis.Redis(host="redis", port=6379)
    r.publish("event", "hello world")
    return HttpResponse()
