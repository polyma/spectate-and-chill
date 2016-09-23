import urllib.request
import urllib.error
import urllib.parse
import json


from .Singleton import Singleton

from .models import TwitchStream, StreamerAccount, Region
from django.conf import settings



@Singleton
class Twitch(object):
    clientId = "6pa8l0sp8lkegpv6azeut88ivayu2my"
    clientSecret="j1ggjzab2k2xgqbsag0ns4ofvkriss4"


    def __init__(self):
        pass
        
        
    def manuallyAddStreamer(self, twitchName, summonerName, summonerRegionSlug):
    
        # Pull the TwitchAccount
        ts = None
        
        try:
            ts = TwitchStream.objects.get(name=twitchName.lower())
        except:
            
            url = "https://api.twitch.tv/kraken/streams/%s"%twitchName
            
            print(url)
            
            twitchJson = None
            try:
                r = urllib.request.Request(url)
                r.add_header("Client-ID", self.clientId)
                response = urllib.request.urlopen(r)

                twitchJson = json.loads(response.read().decode('utf-8'))
            except Exception as e:
                # doesn't exist?
                print("Unable to find streamer: %s"%e)
                return False

            if twitchJson["stream"] == None:
                ts = TwitchStream(
                    name = twitchName.lower(),
                    display_name = twitchName,
                    live = False,
                )
                ts.save()
            else:
                
                logo = ""
                if twitchJson["stream"]["channel"]["logo"] != None:
                    logo = twitchJson["stream"]["channel"]["logo"]
                    
                language = ""
                if twitchJson["stream"]["channel"]["language"] != None:
                    language = twitchJson["stream"]["channel"]["language"]
                    
                status = "Untitled Stream"
                if twitchJson["stream"]["channel"]["status"] != None:
                    status = twitchJson["stream"]["channel"]["status"]
                
                ts = TwitchStream(
                    twitchId = twitchName["channel"]["_id"],
                    name = twitchJson["stream"]["channel"]["name"],
                    display_name = twitchJson["stream"]["channel"]["display_name"],
                    language = language,
                    
                    logo = logo,
                    previewSmall = twitchJson["stream"]["preview"]["small"],
                    previewMedium = twitchJson["stream"]["preview"]["medium"],
                    previewLarge = twitchJson["stream"]["preview"]["large"],
                    
                    status = status,
                    currentViews = twitchJson["stream"]["viewers"],
                    totalViews = twitchJson["stream"]["channel"]["views"],
                    followers = twitchJson["stream"]["channel"]["followers"],
                    
                    live = True,
                )
                
                ts.save()
        
        region = None
        try:
            region = Region.objects.get(slug=summonerRegionSlug.lower())
        except:
            print("Bad match on the region, make sure regions are up-to-date in the DB")
            return False
            
        # get the summoner
        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{name}?api_key={api_key}"

        sendMe = url.format(
            region=region.slug,
            name=summonerName,
            api_key=settings.APIKEY,
        )

        print(sendMe)
        summonerJson = None
        try:
            r = urllib.request.Request(sendMe)
            response = urllib.request.urlopen(r)

            summonerJson = json.loads(response.read().decode('utf-8'))
            
        except urllib.error.HTTPError as e:
            print("Summoner not found")
            return False
            
        try:
            sa = StreamerAccount(
                summonerId = summonerJson[list(summonerJson)[0]]["id"],
                region = region,
                stream = ts,
            )
            sa.save()
        except Exception as e:
            print("Unable to create Summoner Account: %s"%e)
            return False
        
            
        print("Summoner/Streamer added to db")
        return True
        
    
        

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
            
            status = "Untitled Stream"
            if stream["channel"]["status"] != None:
                status = stream["channel"]["status"]
                
            logo = ""
            if stream["channel"]["logo"] != None:
                logo = stream["channel"]["logo"]
                
            language = ""
            if stream["channel"]["language"] != None:
                language = stream["channel"]["language"]
            
            streamer, created = TwitchStream.objects.update_or_create(
                twitchId = stream["_id"],
                name = stream["channel"]["name"],

                defaults = {
                    "display_name":stream["channel"]["display_name"],
                    "language":language,
                    "logo":logo,
                    "status":status,
                    "currentViews":stream["viewers"],
                    "totalViews":stream["channel"]["views"],
                    "followers":stream["channel"]["followers"],
                    "live":True,
                }
            )
            streamers.append(streamer)


        # Do an exclude to find out who's not actively streaming, setting streaming to false
        #notLive = TwitchStream.objects.exclude(primary_key__in=ids)


    def update_TwitchStream(self, stream):
        url = "https://api.twitch.tv/kraken/streams/%s"%stream.name

        twitchJson = None
        try:
            r = urllib.request.Request(url)
            r.add_header("Client-ID", self.clientId)
            response = urllib.request.urlopen(r)

            twitchJson = json.loads(response.read().decode('utf-8'))
        except:
            # doesn't exist?
            return stream

        if "stream" in twitchJson and twitchJson["stream"] != None:
            # They have content to update
            stream.display_name = twitchJson["stream"]["channel"]["display_name"]
            
            language = ""
            if twitchJson["stream"]["channel"]["language"] != None:
                language = twitchJson["stream"]["channel"]["language"]
            
            logo = ""
            if twitchJson["stream"]["channel"]["logo"] != None:
                logo = twitchJson["stream"]["channel"]["logo"]

            status = "Untitled Stream"
            if twitchJson["stream"]["channel"]["status"] != None:
                status = twitchJson["stream"]["channel"]["status"]
                
            stream.language = language
                
            stream.logo = logo
            stream.previewSmall = twitchJson["stream"]["preview"]["small"]
            stream.previewMedium = twitchJson["stream"]["preview"]["medium"]
            stream.previewLarge = twitchJson["stream"]["preview"]["large"]

            stream.status = status
            stream.currentViews = twitchJson["stream"]["viewers"]
            stream.totalViews = twitchJson["stream"]["channel"]["views"]
            stream.followers = twitchJson["stream"]["channel"]["followers"]

        else:
            stream.live=False

        stream.save()
        return stream





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
        streamersJson = json.loads(response.read().decode('utf-8'))

        streamers = {} # converted to list later

        while len(streamersJson["streams"]) > 0:
            # Process
            for stream in streamersJson["streams"]:
                #print("len before: %s"%len(list(streamers)))

                logo = ""
                if stream["channel"]["logo"] != None:
                    logo = stream["channel"]["logo"]

                language = ""
                if stream["channel"]["language"] != None:
                    language = stream["channel"]["language"]
                    
                status = "Untitled Stream"
                if stream["channel"]["status"] != None:
                    status = stream["channel"]["status"]
                    
                streamers.update(
                    {stream["channel"]["name"]:
                        {
                        "id":stream["_id"],
                        "name":stream["channel"]["name"],
                        "display_name":stream["channel"]["display_name"],
                        "language":language,

                        "logo":logo,
                        "previewSmall":stream["preview"]["small"],
                        "previewMedium":stream["preview"]["medium"],
                        "previewLarge":stream["preview"]["large"],

                        "status":status,
                        "currentViews":stream["viewers"],
                        "totalViews":stream["channel"]["views"],
                        "followers":stream["channel"]["followers"],
                        }
                    }
                )
                #print("len after: %s"%len(list(streamers)))

            # Issue the new call
            offset += limit
            url = "https://api.twitch.tv/kraken/streams?game=League%%20of%%20Legends&stream_type=live&limit=%s&offset=%s"%(limit, offset)
            print("Streamers: %s"%len(list(streamers)))

            try:
                r = urllib.request.Request(url)
                r.add_header("Client-ID", self.clientId)
                response = urllib.request.urlopen(r)

                streamersJson = json.loads(response.read().decode('utf-8'))
            except:
                break
        print("Streamers: %s"%len(list(streamers)))

        print("Checking against the summoner names")

        # Split the streamer names into lists of 40, ideal for checking names
        streamersList = list(streamers)
        splitLists = [streamersList[x:x+40] for x in range(0, len(streamersList), 40)]
        #region = "na"
        url = "https://{region}.api.pvp.net/api/lol/{region}/v1.4/summoner/by-name/{names}?api_key={api_key}"

        summoners = []
        summonerNamesFound = 0

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
                                "summonerName":summonersJson[streamerName]["name"],
                                "summonerId":summonersJson[streamerName]["id"],
                            }
                        )
                        summonerNamesFound += 1
                    else:
                        summoners.append(None)
            except:
                for _ in range(len(sublist)):
                    summoners.append(None)

        print("Summoner Names obtained: %s"%summonerNamesFound)


        # Check if these guys are in game
        #region_tag = "NA1"
        url = "https://{region}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{region_tag}/{summoner_id}?api_key={api_key}"


        for i in range(len(summoners)):
            if summoners[i] == None:
                continue

            sendMe = ""
            try:
                sendMe = url.format(
                    region=region.slug,
                    region_tag=region.region_tag.upper(),
                    summoner_id=summoners[i]["summonerId"],
                    api_key=settings.APIKEY,
                )
            except Exception as e:
                print("Phase 1: %s"%e)
                continue


            gameJson = None

            try:
                r = urllib.request.Request(sendMe)
                response = urllib.request.urlopen(r)

                gameJson = json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                continue

            ts = None
            try:
                # They exist
                #print("Adding player to db")

                # Create a TwitchStream object
                streamer = streamers[streamersList[i]]
                #print(streamer)
                logo = ""
                if "logo" in streamer and streamer["logo"] != None:
                    logo = streamer["logo"]
                ts, created = TwitchStream.objects.update_or_create(
                    twitchId = streamer["id"],
                    name = streamer["name"],
                    defaults = {
                        "display_name":streamer["display_name"],
                        "language":language,

                        "logo":logo,
                        "previewSmall":streamer["previewSmall"],
                        "previewMedium":streamer["previewMedium"],
                        "previewLarge":streamer["previewLarge"],

                        "status":streamer["status"],
                        "currentViews":streamer["currentViews"],
                        "totalViews":streamer["totalViews"],
                        "followers":streamer["followers"],

                        "matchId":gameJson["gameId"],
                        "live":True,
                    }
                )
                ts.save()
            except Exception as e:
                print("Exception creating Twitch Stream: %s"%e)
                continue
                
            try:
                # Save them into the db
                stream, created = StreamerAccount.objects.update_or_create(
                    summonerId = summoners[i]["summonerId"],
                    region = region,

                    defaults = {
                        #"streamId":ts.twitchId,
                        #"streamName":ts.name,
                        "stream":ts
                    }
                )
                stream.save()



            except Exception as e:
                print("Exception creating streamer: %s"%e)
                print("len(matchId): %s"%gameJson["gameId"])
                print("len(summoner): %s"%summoners[i]["summonerId"])
                
        streamerCount = TwitchStream.objects.all().count()
        accountCount = StreamerAccount.objects.all().count()
        print("Total of %s streamers with %s accounts now in the database"%(streamerCount, accountCount))
