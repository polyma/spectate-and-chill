#import threading

#from cassiopeia import baseriotapi
#from cassiopeia.type.core.currentgame import Game


from .Singleton import Singleton
from .twitch import Twitch
from .models import *
import time
import redis
from django.conf import settings

redisServer = settings.IP_ADDRESS


@Singleton
class Check_Current_Games(objects):
    def __init__(self):
        self.twitchApi = Twitch.Instance()
        
    def loopManager(self):
        while true:
            self.checkAllGames()
            time.sleep(120)
        
    def checkAllGames(self):
        streamers = Streamer.objects.all()
        url = "https://{region}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{region_tag}/{summoner_id}?api_key={api_key}"
        
        for streamer in streamers:
            # Check if they're in game
            sendMe = url.format(
                region=streamer.region.slug,
                region_tag=streamer.region.region_tag.upper(),
                summoner_id=streamer.summonerId,
                api_key=settings.APIKEY,
            )
            
            gameJson = None
            try:
                r = urllib.request.Request(sendMe)
                response = urllib.request.urlopen(r)
                
                gameJson = json.loads(response.read().decode('utf-8'))
                
                # They're in a game
                streamer.matchId = gameJson["gameId"]
            except urllib.error.HTTPError as e:
                # They're not in a game
                streamer.matchId = "0"
                
                
                
            streamer.save()
    
        # Streamers who have all of their accounts with a matchId == 0, set TwitchStream offline
        twitchStreams = TwitchStream.objects.all()
        for ts in twitchStreams:
            streamerAccounts = Streamer.objects.filter(streamId=ts.twitchId, streamName=ts.name)
            if streamerAccounts.count() == 0:
                ts.live = False
            else:
                ts.live = True
                # Update the TwitchStream based on the API
            ts.save()
            
        
        
        
        # Redis Update Goes Here        

            
def schedule_checks(region, summoner_ids, on_new_game, minutes_per_check=2):
    __do_check(region, summoner_ids, on_new_game, minutes_per_check)


def __do_check(region, summoner_ids, on_new_game, minutes_per_check):
    baseriotapi.set_region(region)

    for summoner_id in summoner_ids:
        try:
            current_game = baseriotapi.get_current_game(summoner_id)
        except:
            current_game = None

        if current_game:
            on_new_game(Game(current_game))

    timer = threading.Timer(60 * minutes_per_check, __do_check, [region, summoner_ids, on_new_game, minutes_per_check])
    timer.daemon = True
    timer.start()
