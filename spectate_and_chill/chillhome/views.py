from django.shortcuts import render
from django.http import HttpResponse, Http404

import urllib.request
import urllib.error
import urllib.parse 
import json
import time
import redis

from cassiopeia import baseriotapi, riotapi
from django.conf import settings

redisServer = settings.IP_ADDRESS
#redisServer = "54.183.202.43"
#redisServer = "redis"

from .models import *

# Create your views here.
def index(request):
    #return HttpResponse("You made it!")
    return render(request, 'chillhome/index.html')


def request_summoner(request):
    # ?summonerName={name}&region={region}

    summoner = None
    created = False
    try:
        # Request the API
        region = (request.GET.get("region")).lower()
        summonerName = request.GET.get("summonerName")

        #baseriotapi.set_region(region)
        #summoner = riotapi.get_summoner_by_name(summonerName)

        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{name}?api_key={apikey}".format(
            region=region,
            name=summonerName,
            apikey=settings.APIKEY,
        )
        r = urllib.request.Request(url)
        response = urllib.request.urlopen(r)
        
        j = json.loads(response.read().decode('utf-8'))
        
        summonerJson = j[list(j)[0]]
        
        summoner, created = User.objects.update_or_create(
            summonerId = summonerJson["id"],
            region = region,
            default = {
                "summonerName":summonerJson["name"],
                "summonerIcon":summonerJson["profileIconId"],
                "summonerSimpleName":summonerName,
            }
        )

    except:
        # Something was wrong or went wrong, assume the summoner doesn't exist
        raise Http404('Invalid Summoner')
        
    try:
        if created:
            # New user, new recommendations
            pass
            
        
    
        #dummyData = [{
        #        "id": "streamer",
        #        "displayName":"MushIsGosu",
        #        "name":"muchisgosu",
        #        "language":"en",
        #        "logo":"https://static-cdn.jtvnw.net/jtv_user_pictures/mushisgosu-profile_image-b1c8bb5fd700025e-300x300.png",
        #        "status":"TSM Gosu - Solo Q - Shadowverse later",
        #        "currentViews":7333,
        #        "totalViews":78560127,
        #        "followers":1096293,
        #
        #        "spectateURL":"<complete gibberish>",
        #        "twitchURL":"https://www.twitch.tv/mushisgosu",
        #        "previewURL_small":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-80x45.jpg",
        #        "previewURL_medium":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-320x180.jpg",
        #        "previewURL_large":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-640x360.jpg",
        #        "championId":67,
        #        "lane":"",
        #        "followedBy":[{
        #            "id": "%s_%s"%(summoner.id, region),
        #            "summonerId":summoner.id,
        #            "region":region,
        #        }]
        #}]
        #r = redis.Redis(host=redisServer, port=6379)
        #r.publish("event", json.dumps(dummyData))
        #return HttpResponse()
    except Exception as e:
        raise Http404('KABOOM \n%s'%e)


def delay404(request):
    time.sleep(5)
    raise Http404()

def redisTest(request):
    r = redis.Redis(host=redisServer, port=6379)
    r.publish("event", "hello world")
    return HttpResponse()

def recommendations(request):
    region = ""
    summonerName = ""
    try:
        region = (request.GET.get("region")).lower()
        summonerName = request.GET.get("summonerName")
    except:
        raise Http404("Must provide region and summonerName")
        
    user = None
    try:
        user = User.objects.get(region=region, summonerSimpleName=summonerName)
    except:
        raise Http404("No such summoner in DB")
        

    # Return recommendations
    recommendations = Recommendation.objects.filter(User=user)
    
    content = []
    for recommended in recommendations:
        info = {}
        info["score"] = recommended.score
        info["streamerName"] = recommended.streamer.streamName
        content.append(info)
        
    
    return HttpResponse(json.dumps(content))

        
    #dummyData = [
    #        {
    #            "summonerName":"Hi Im Gosu",
    #            "region":"na",
    #            "name":"muchisgosu",
    #            "displayName":"MushIsGosu",
    #        },
    #        {
    #            "summonerName":"Voyboy",
    #            "region":"na",
    #            "name":"voyboy",
    #            "displayName":"Voyboy",
    #        }
    #]
    #return HttpResponse(json.dumps(dummyData))
    
