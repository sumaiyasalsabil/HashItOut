from django.db import models

# Create your models here.

class BrainWave(models.Model):
    name = models.CharField(max_length=400)

class WavePoint(models.Model):
    wave = models.ForeignKey(BrainWave, on_delete=models.CASCADE)

class WaveTime(models.Model):
    point = models.ForeignKey(WavePoint, on_delete=models.CASCADE)
    time = models.FloatField()

class WaveValue(models.Model):
    point = models.ForeignKey(WavePoint, on_delete=models.CASCADE)
    value = models.FloatField()