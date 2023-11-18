from django.db import models

# Create your models here.

class BrainWave(models.Model):
    name = models.CharField(max_length=400)

class WavePoint(models.Model):
    wave = models.ForeignKey(BrainWave, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    time = models.FloatField()