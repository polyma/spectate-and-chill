import urllib.request
import urllib.error
import urllib.parse 
import json


from .Singleton import Singleton

from .models import TwitchStreamer, Streamer
from django.conf import settings



@Singleton
class Twitch(object):
    clientId = "6pa8l0sp8lkegpv6azeut88ivayu2my"
    clientSecret="j1ggjzab2k2xgqbsag0ns4ofvkriss4"

    
    def __init__(self):
        pass
        
    def _current_streamers(self, offset=0, limit=100):
        url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
        
        r = urllib.request.Request(url)
        r.add_header("Client-ID", self.clientId)
        response = urllib.request.urlopen(r)
        
        j = json.loads(response.read().decode('utf-8'))
        totalStreams = j["_total"]
        
        # Repeat until all streamers pulled
        streamers = []
        ids = []
        
        for stream in j["streams"]:
            ids.append(stream["_id"])
            streamer, created = TwitchStreamer.objects.update_or_create(
                twitchId = stream["_id"],
                name = stream["channel"]["name"],
                
                defaults = {
                    "display_name":stream["channel"]["display_name"],
                    "language":stream["channel"]["language"],
                    "logo":stream["channel"]["logo"],
                    "status":stream["channel"]["status"],
                    "currentViews":stream["viewers"],
                    "totalViews":stream["channel"]["views"],
                    "followers":stream["channel"]["followers"],
                    "live":True,
                }
            )
            streamers.append(streamer)
        
        
        # Do an exclude to find out who's not actively streaming, setting streaming to false
        #notLive = TwitchStreamer.objects.exclude(primary_key__in=ids)
        
        
        
    def _get_stream(self, name):
        url = "https://api.twitch.tv/kraken/streams/%s"%name
        
        r = urllib.request.Request(url)
        r.add_header("Client-ID", self.clientId)
        response = urllib.request.urlopen(r)
        
        j = json.loads(response.read().decode('utf-8'))
        
        
        if "stream" in j and len(j["stream"]) > 0:
            # They're streaming, but is it League?
            if j["stream"]["game"] != "League of Legends":
                return {}
                
            streamInfo = {
                "language":j["stream"]["channel"]["language"],
                "displayName":j["stream"]["channel"]["display_name"],
                "status":j["stream"]["channel"]["status"],
            
                # Views
                "currentViews":j["stream"]["viewers"],
                "lifetimeViews":j["stream"]["channel"]["views"],
                "followers":j["stream"]["channel"]["followers"],
                
                
                # Images
                "smallPreview":j["preview"]["small"],
                "mediumPreview":j["preview"]["medium"],
                "largePreview":j["preview"]["large"],
                "logo":j["channel"]["logo"],
            }
            return streamInfo
            
                
        return {}
            
        
    def autofind_streamers(self):
        limit = 100
        offset = 0
        url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
        
        r = urllib.request.Request(url)
        r.add_header("Client-ID", self.clientId)
        response = urllib.request.urlopen(r)
        j = json.loads(response.read().decode('utf-8'))
        
        streamers = set([]) # converted to list later
        
        while len(j["streams"]) > 0:
            # Process
            for stream in j["streams"]:
                streamers.add(stream["channel"]["name"])
            
            # Issue the new call
            offset += limit
            url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
            
            r = urllib.request.Request(url)
            r.add_header("Client-ID", self.clientId)
            response = urllib.request.urlopen(r)
            
            j = json.loads(response.read().decode('utf-8'))
        
        
        # Split the streamer names into lists of 40, ideal for checking names
        streamers = list(streamers)
        splitLists = [streamers[x:x+40] for x in range(0, len(streamers), 40)]
        region = "na"
        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{names}?api_key={api_key}"
        
        summoners = 
        
        for sublist in splitLists:
            url = url.format(
                region=region,
                names=",".join(sublist),
                api_key=settings.APIKEY,
            )
        
            try:
                r = urllib.request.Request(url)
                response = urllib.request.urlopen(r)
                
                
                
            except:
                pass
            
        
        
        
        
    def _whos_streaming(self):    
        limit = 100
        offset = 0
        url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
        
        r = urllib.request.Request(url)
        r.add_header("Client-ID", self.clientId)
        response = urllib.request.urlopen(r)
        
        j = json.loads(response.read().decode('utf-8'))
        
        streamers = set([])
        
        while len(j["streams"]) > 0:
            # Process
            for stream in j["streams"]:
                streamers.add(stream["channel"]["name"])
            
            # Issue the new call
            offset += limit
            url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
            
            r = urllib.request.Request(url)
            r.add_header("Client-ID", self.clientId)
            response = urllib.request.urlopen(r)
            
            j = json.loads(response.read().decode('utf-8'))
        
        from cassiopeia import baseriotapi, riotapi
        riotapi.set_load_policy("lazy")
        riotapi.set_rate_limit(25000, 10)
        riotapi.set_data_store(None)
        riotapi.set_api_key("RGAPI-e4491f0b-b99a-49c4-b817-5f9b00267da1")
        
        
        streamers = list(streamers)
        
        baseriotapi.set_region("na")
        summoners = riotapi.get_summoners_by_name(streamers)
        
        # print("Streamers: %s\nSummoners: %s"%(len(streamers),len(summoners)))
        
        inGame = []
        
        for i in range(len(summoners)):
            if summoners[i]:
                hit = riotapi.get_current_game(summoners[i])
                if hit:
                    data = hit.data
                    champion = 0
                    for participant in data.participants:
                        if participant.summonerId == summoners[i].id:
                            champion = participant.championId
                            
                        
                    #inGame.append({"streamer":streamers[i], "champion":
                    print("%s is in game playing %s"%(streamers[i], champion))
            #except Exception as e:
            #    print(e)
            #    pass
        
    