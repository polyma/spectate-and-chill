import urllib.request
import urllib.error
import urllib.parse 
import json


from .Singleton import Singleton

from .models import TwitchStreamer


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
        streamers = append[]
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
        notLive = TwitchStreamer.objects.exclude(primary_key__in=ids)
        
        
        
        
        
        
        