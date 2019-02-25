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

class blocks(models.Model):
    number = models.IntegerField()
    timestamp = models.DateTimeField()  

class votes(models.Model):
    voter = models.TextField()
    author = models.TextField()
    permlink = models.TextField()
    weight = models.IntegerField()
    value = models.FloatField(default=0)
    timestamp = models.DateTimeField()  

class transfers_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class transfers_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class transfers_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class transfers(models.Model):
    sender = models.TextField()
    receiver = models.TextField()
    amount = models.IntegerField()
    precision = models.FloatField()
    nai = models.TextField()
    timestamp = models.DateTimeField() 

class claim_rewards_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class claim_rewards_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class claim_rewards_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField()

class claim_rewards(models.Model):
    account = models.TextField()
    reward_steem = models.TextField()
    reward_sbd = models.TextField()
    reward_vests = models.TextField()
    timestamp = models.DateTimeField() 