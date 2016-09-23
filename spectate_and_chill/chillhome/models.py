from django.db import models
from django.contrib.postgres.fields import JSONField


class Region(models.Model):
    slug = models.CharField(primary_key=True, max_length=4)
    region_tag = models.CharField(max_length=5)
    hostname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class Language(models.Model):
    region = models.ForeignKey(Region)
    locale = models.CharField(max_length=5)

#class MatchEverything(models.Model):
#    matchId = models.PositiveIntegerField() #Long?
#    region = models.ForeignKey(Region)
#    json = JSONField()
#
#    # Primary key is the matchId + region
#    def __str__(self):
#        return "MatchEverything (%s %s)"%(self.matchId, self.region)
#
#    class Meta:
#        unique_together = ("matchId", "region")

class TwitchStream(models.Model):
    twitchId = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    language = models.CharField(max_length=5, default="", blank=True)

    logo = models.CharField(max_length=250, blank=True)
    previewSmall = models.CharField(max_length=250, blank=True)
    previewMedium = models.CharField(max_length=250, blank=True)
    previewLarge = models.CharField(max_length=250, blank=True)

    status = models.CharField(max_length=150, default="")
    currentViews = models.PositiveIntegerField(default=0)
    totalViews = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)


    championId = models.IntegerField(default=0)
    matchId = models.CharField(max_length=15, default="0")
    regionSlug = models.CharField(max_length=4, default="")
    encryptionKey = models.CharField(max_length=40, default="")

    live = models.BooleanField(default=False)


class StreamerAccount(models.Model):
    summonerId = models.PositiveIntegerField()
    region = models.ForeignKey(Region)

    stream = models.ForeignKey(TwitchStream)

    #streamId = models.CharField(max_length=20, default=0)
    #streamName = models.CharField(max_length=50, default="")

    class Meta:
        unique_together = ("summonerId", "region")


class User(models.Model):
    summonerId = models.PositiveIntegerField()
    region = models.ForeignKey(Region)
    summonerName = models.CharField(max_length=24)
    summonerSimpleName = models.CharField(max_length=24) # What the query string passes in
    summonerIcon = models.PositiveIntegerField()

    class Meta:
        unique_together = ("summonerId", "region")


class Recommendation(models.Model):
    user = models.ForeignKey(User)
    streamer = models.ForeignKey(StreamerAccount)
    score = models.FloatField()

    class Meta:
        unique_together = ("user", "streamer")
