import urllib.request
import urllib.error
import urllib.parse 
import json


from .Singleton import Singleton

from .models import TwitchStreamer, Streamer, Region
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
            streamer, created = TwitchStream.objects.update_or_create(
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
        #notLive = TwitchStream.objects.exclude(primary_key__in=ids)
        
        
        
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
        
        region = Region.objects.get(slug="na")
        
        r = urllib.request.Request(url)
        r.add_header("Client-ID", self.clientId)
        response = urllib.request.urlopen(r)
        j = json.loads(response.read().decode('utf-8'))
        
        streamers = {} # converted to list later
        
        while len(j["streams"]) > 0:
            # Process
            for stream in j["streams"]:
                streamers.update(
                    {stream["channel"]["name"]:
                        {
                        "id":stream["_id"], 
                        "name":stream["channel"]["name"],
                        "display_name":stream["channel"]["display_name"],
                        "language":stream["channel"]["language"], 
                        "logo":stream["channel"]["logo"],
                        "status":stream["channel"]["status"],
                        "currentViews":stream["viewers"],
                        "totalViews":stream["channel"]["views"],
                        "followers":stream["channel"]["followers"],
                        }
                    }
                )
            
            # Issue the new call
            offset += limit
            url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
            
            r = urllib.request.Request(url)
            r.add_header("Client-ID", self.clientId)
            response = urllib.request.urlopen(r)
            
            streamersJson = json.loads(response.read().decode('utf-8'))

        # Split the streamer names into lists of 40, ideal for checking names
        streamersList = list(streamers)
        splitLists = [streamersList[x:x+40] for x in range(0, len(streamersList), 40)]
        #region = "na"
        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{names}?api_key={api_key}"
        
        summoners = []
        
        for sublist in splitLists:
            sendMe = url.format(
                region=region.slug,
                names=",".join(sublist),
                api_key=settings.APIKEY,
            )
        
            try:
                r = urllib.request.Request(sendMe)
                response = urllib.request.urlopen(r)
                
                summonersJson = json.loads(response.read().decode('utf-8'))
                
                for streamerName in sublist:
                    if streamerName in summonersJson:
                        summoners.append(
                            {
                                "summonerName":summonerJson[streamerName]["name"],
                                "summonerId":summonerJson[streamerName]["id"],
                            }
                        )
                        
                    else:
                        summoners.append(None)
            except:
                for _ in range(len(sublist)):
                    summoners.append(None)
                    
        # Check if these guys are in game
        #region_tag = "NA1"
        url = "https://{region}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{region_tag}/{summoner_id}?api_key={api_key}"
              
        
        for i in range(len(summoners)):
            sendMe = url.format(
                region=region.slug,
                region_tag=region.region_tag,
                summoner_id=summoners[i]["summonerId"],
                api_key=settings.APIKEY,
            )
        
            try:
                r = urllib.request.Request(sendMe)
                response = urllib.request.urlopen(r)
                
                gameJson = json.loads(response.read().decode('utf-8'))
                
                # They exist
                
                # Create a TwitchStream object
                streamer = streamers[streamersList[i]]
                
                ts, created = TwitchStream.objects.update_or_create(
                    twitchId = streamer["id"],
                    name = streamer["name"],
                    defaults = {
                        "display_name":streamer["display_name"],
                        "language":streamer["language"],
                        "logo":streamer["logo"],
                        "status":streamer["status"],
                        "currentViews":streamer["currentViews"],
                        "totalViews":streamer["totalViews"],
                        "followers":streamer["followers"],
                        "live":True,
                    }
                )
                ts.save()
                
                # Save them into the db
                stream, created = Streamer.objects.update_or_create(
                    summonerId = summoners[i]["summonerId"],
                    region = region,
                    
                    defaults = {
                        "matchId":gameJson["gameId"],
                        "streamId":ts.twitchId,
                        "streamName":ts.name,
                    }
                )
                stream.save()
                
                
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
        
    