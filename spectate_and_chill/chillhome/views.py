from django.shortcuts import render
from django.http import HttpResponse, Http404

import urllib.request
import urllib.error
import urllib.parse
import json
import time
import redis

from .recommend import Recommender

from cassiopeia import baseriotapi, riotapi
from django.conf import settings

redisServer = settings.IP_ADDRESS
#redisServer = "54.183.202.43"
#redisServer = "redis"

from .models import *



def pullRegions():
    url = "http://status.leagueoflegends.com/shards"
    r = urllib.request.Request(url)
    response = urllib.request.urlopen(r)

    shards = json.loads(response.read().decode('utf-8'))

    for shard in shards:
        region, created = Region.objects.get_or_create(
            slug=shard["slug"],
            defaults={
                "region_tag":shard["region_tag"],
                "hostname":shard["hostname"],
                "name":shard["name"],
            }
        )

        if region.slug == 'euw':
            region.region_tag = 'euw1'
            region.save()
            

        
        for locale in shard["locales"]:
            lang, created = Language.objects.get_or_create(
                region = region,
                locale = locale
            )




def index(request):
    #return HttpResponse("You made it!")
    return render(request, 'chillhome/index.html')


def request_summoner(request):
    # ?summonerName={name}&region={region}

    summoner = None
    created = False

    region = None
    summonerName = None
    try:
        # Request the API
        region = (request.GET.get("region")).lower()
        summonerName = request.GET.get("summonerName")
    except:
        raise Http404("Must provide region and summonerName")

    try:
        region = Region.objects.get(slug=region)
    except:
        pullRegions()

        try:
            region = Region.objects.get(slug=region)
        except:
            raise Http404("Invalid Region: %s"%region)


    try:
        print(region.slug, summonerName)

        #baseriotapi.set_region(region)
        #summoner = riotapi.get_summoner_by_name(summonerName)

        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{name}?api_key={apikey}".format(
            region=region.slug,
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
            defaults = {
                "summonerName":summonerJson["name"],
                "summonerIcon":summonerJson["profileIconId"],
                "summonerSimpleName":summonerName,
            }
        )
        summoner.save()

    except Exception as e:
        # Something was wrong or went wrong, assume the summoner doesn't exist
        #print(e)
        raise Http404('Invalid Summoner')

    return HttpResponse(summoner.summonerSimpleName);
        #dummyData = [{
        #       "id": "streamer",
        #       "displayName":"MushIsGosu",
        #       "name":"muchisgosu",
        #       "language":"en",
        #       "logo":"https://static-cdn.jtvnw.net/jtv_user_pictures/mushisgosu-profile_image-b1c8bb5fd700025e-300x300.png",
        #       "status":"TSM Gosu - Solo Q - Shadowverse later",
        #       "currentViews":7333,
        #       "totalViews":78560127,
        #       "followers":1096293,
        #
        #       "spectateURL":"<complete gibberish>",
        #       "twitchURL":"https://www.twitch.tv/mushisgosu",
        #       "previewURL_small":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-80x45.jpg",
        #       "previewURL_medium":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-320x180.jpg",
        #       "previewURL_large":"https://static-cdn.jtvnw.net/previews-ttv/live_user_mushisgosu-640x360.jpg",
        #       "championId":67,
        #       "lane":"",
        #}]
        # r = redis.Redis(host=redisServer, port=6379)
        # r.publish("event", json.dumps(dummyData))
        #return HttpResponse(json.dumps(dummyData))
    #except Exception as e:
    #    raise Http404('KABOOM \n%s'%e)


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

    try:
        region = Region.objects.get(slug=region)
    except:
        pullRegions()

        try:
            region = Region.objects.get(slug=region)
        except:
            raise Http404("Invalid Region: %s"%region)

    user = None
    try:
        user = User.objects.get(region=region, summonerSimpleName=summonerName)
    except:
        raise Http404("No such summoner in DB")



    #try:
    if True:
    #if created:
        # New user, new recommendations
        # Pull Champion Mastery for this user
        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{name}?api_key={apikey}".format(
            region=region.slug,
            name=summonerName,
            apikey=settings.APIKEY,
        )
        r = urllib.request.Request(url)
        response = urllib.request.urlopen(r)
        j = json.loads(response.read().decode('utf-8'))
        summonerJson = j[list(j)[0]]
        print(summonerJson)
        summonerId = summonerJson["id"]
        
        
        url = "https://{region}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/champions?api_key={apikey}".format(
        region=region.slug,
        platform=region.region_tag.upper(),
        summonerId=summonerId,
        apikey=settings.APIKEY,
        )
        r = urllib.request.Request(url)
        response = urllib.request.urlopen(r)
        champMastery = json.loads(response.read().decode('utf-8'))
        print (champMastery)

        #TODO: REPLACE TRY EXCEPT HERE
        recommender = Recommender.from_file("chillhome/model.pkl")
        #recommender = (RecommenderWrapper.Instance()).recommender
        response = recommender.recommend({"id":summonerId, "region":region}, champMastery)

        #     response = [{"id":"adil", "region":region, "score": 1.0},{"id":"streamer", "region":region, "score": 1.0}]
        print(response)

        for r in response:
            # Find the streamer
            streamer, created = Streamer.objects.get_or_create(
                summonerId = r["id"],
                region = Region.objects.get(slug=r["region"].lower()),
            )

            streamer.save()

            # Save the response
            recommendation, created = Recommendation.objects.update_or_create(
                user=summoner,
                streamer = streamer,
                defaults={
                    "score":r["score"],
                }
            )

            recommendation.save()

        # Pull the recommendations from the DB
        recommendations = Recommendation.objects.filter(user=summoner).order_by("score")
        print("Recommendations: %s"%recommendations)

        content = []
        for r in recommendations:
            content.append({
                "twitchName":r.streamer.streamName,
                "summonerId":r.streamer.summonerId,
                "region":r.streamer.region.slug,
            })


        return HttpResponse(json.dumps(content))
    # # Return recommendations
    # recommendations = Recommendation.objects.filter(User=user)
    #
    # content = []
    # for recommended in recommendations:
    #     info = {}
    #     info["score"] = recommended.score
    #     info["streamerName"] = recommended.streamer.streamName
    #     content.append(info)
    #
    #
    # return HttpResponse(json.dumps(content))


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
