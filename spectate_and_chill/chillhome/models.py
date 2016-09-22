from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class MatchEverything(models.Model):
    matchId = models.IntegerField() #Long?
    region = models.CharField(max_length=4)
    json = JSONField() # Double Check
    
    # Primary key is the matchId + region 
    
class TwitchStreamer(models.Model):
    pass
    
    