from django.db import models

class votes_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class votes_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class votes_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()


