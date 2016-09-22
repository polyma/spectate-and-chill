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
    dummyData = [
        "streamer":{
            "displayName":"MushIsGosu",
            "name":"muchisgosu",
            "language":"en",
            "logo":"https://static-cdn.jtvnw.net/jtv_user_pictures/mushisgosu-profile_image-b1c8bb5fd700025e-300x300.png",
            "status":"TSM Gosu - Solo Q - Shadowverse later",
            "currentViews":7333,
            "totalViews":78560127,
            "followers":1096293, 
            
            "followedBy":[{
                "summonerId":123456789,
                "region":"na",
            }]
        }
    ]
    r = redis.Redis(host="redis", port=6379)
    r.publish("event", json.dumps(dummyData))
    return HttpResponse()

def delay404(request):
    time.sleep(5)
    raise Http404()

def redisTest(request):
    r = redis.Redis(host="redis", port=6379)
    r.publish("event", "hello world")
    return HttpResponse()
