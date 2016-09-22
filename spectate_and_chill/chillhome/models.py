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
    twitchId = models.IntegerField()
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)
    
    