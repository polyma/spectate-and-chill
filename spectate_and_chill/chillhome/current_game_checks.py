import threading

#from cassiopeia import baseriotapi
#from cassiopeia.type.core.currentgame import Game


from .Singleton import Singleton
from .twitch import Twitch
from .models import *
import time
import redis
from django.conf import settings
import urllib.request
import urllib.error
import urllib.parse
import json


redisServer = settings.IP_ADDRESS


@Singleton
class Check_Current_Games(object):
    def __init__(self):
        self.twitchApi = Twitch.Instance()
        # self.twitchApi.autofind_streamers()
        self.running = True


    def checkAllGames(self):
        print ('NOW RUNNING CHECK GAMES')
        streamers = TwitchStream.objects.all()
        url = "https://{region}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{region_tag}/{summoner_id}?api_key={api_key}"

        for streamer in streamers:
            print(streamer)
            # Check their connected StreamerAccounts
            streamer = self.twitchApi.update_TwitchStream(streamer)

            streamer.matchId = "0"
            streamer.regionSlug = ""
            streamer.encryptionKey = ""
            streamer.championId = 0

            accounts = StreamerAccount.objects.filter(stream=streamer)
            for account in accounts:
                # Check if they're in game
                sendMe = url.format(
                    region=account.region.slug,
                    region_tag=account.region.region_tag.upper(),
                    summoner_id=account.summonerId,
                    api_key=settings.APIKEY,
                )

                gameJson = None
                try:
                    r = urllib.request.Request(sendMe)
                    response = urllib.request.urlopen(r)

                    gameJson = json.loads(response.read().decode('utf-8'))

                    # They're in a game
                    streamer.regionSlug = account.region.slug
                    streamer.matchId = gameJson["gameId"]
                    if "observers" in gameJson and "encryptionKey" in gameJson["observers"]:
                        streamer.encryptionKey = gameJson["observers"]["encryptionKey"]

                    # Find their champion
                    for participant in gameJson["participants"]:
                        if participant["summonerId"] == account.summonerId:
                            streamer.championId = participant["championId"]


                    streamer.save()
                    break # No need to see the rest of their games
                except urllib.error.HTTPError as e:
                    # They're not in a game on this account
                    pass


        # Convert all streamers to a list
        streamers = TwitchStream.objects.all()

        content = []
        for streamer in streamers:
            item = {}
            item["id"] = streamer.twitchId
            item["displayName"] = streamer.display_name
            item["name"] = streamer.name
            item["language"] = streamer.language
            item["logo"] = streamer.logo
            item["status"] = streamer.status
            item["currentViews"] = streamer.currentViews
            item["totalViews"] = streamer.totalViews
            item["followers"] = streamer.followers
            item["twitchLive"] = streamer.live

            item["matchId"] = streamer.matchId
            item["region"] = streamer.regionSlug
            item["encryptionKey"] = streamer.encryptionKey
            item["twitchURL"] = "https://www.twitch.tv/%s"%streamer.name
            item["previewURL_small"] = streamer.previewSmall
            item["previewURL_medium"] = streamer.previewMedium
            item["previewURL_large"] = streamer.previewLarge
            item["championId"] = streamer.championId

            content.append(item)

        print(json.dumps(content))

        # Redis Update Goes Here
        r = redis.Redis(host=redisServer, port=6379)
        r.publish("event", json.dumps(content))


        timer = threading.Timer(60 * 2, self.checkAllGames)
        timer.daemon = True
        timer.start()



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
