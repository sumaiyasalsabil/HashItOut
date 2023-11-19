from django.db import models

# Create your models here.

class StartButton(models.Model):
    clicked = models.BooleanField(default=False)