from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class MatchEverything(models.Model):
    matchId = models.IntegerField() #Long?
    region = models.CharField(max_length=4)
    json = JSONField()

    # Primary key is the matchId + region
    def __str__(self):
        return "MatchEverything (%s %s)"%(self.matchId, self.region)

    class Meta:
        unique_together = ("matchId", "region")

class TwitchStreamer(models.Model):
    twitchId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    language = models.CharField(max_length=5)
    logo = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    currentViews = models.IntegerField()
    totalViews = models.IntegerField()
    followers = models.IntegerField()

    live = models.BooleanField(default=False)

    
class Streamer(models.Model):
    summonerId = models.IntegerField()
    region = models.CharField(max_length=4)
    streamService = models.CharField(max_length=10)
    streamId = models.IntegerField()
    streamName = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ("streamService","streamId")
    
    
class User(models.Model):
    summonerId = models.IntegerField()
    region = models.CharField(max_length=4)
    summonerName = models.CharField(max_length=24)
    summonerSimpleName = models.CharField(max_length=24) # What the query string passes in
    summonerIcon = models.IntegerField()
    
    class Meta:
        unique_together = ("summonerId", "region")
    
    
class Recommendation(models.Model):
    user = models.ForeignKey(User)
    streamer = models.ForeignKey(Streamer)
    score = models.FloatField()
    
    class Meta:
        unique_together = ("user", "streamer")
    
    