from django.db import models

# Create your models here.

class MatchEverything(models.Model):
    matchId = Models.IntergerField() #Long?
    region = Models.CharField()
    json = Models.JsonField() # Double Check
    
    # Primary key is the matchId + region 
    
class TwitchStreamer(models.Model):
    pass
    
    