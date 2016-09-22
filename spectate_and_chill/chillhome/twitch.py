import urllib.request
import urllib.error
import urllib.parse 
import json


from .Singleton import Singleton


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
        
        
        
        
        
        
        