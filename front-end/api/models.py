from django.db import models

class votes_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class votes_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class votes_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class votes_count_sum(models.Model):
    analyses = models.CharField(db_index=True, max_length=10)
    resolution = models.CharField(db_index=True, max_length=10)
    data = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

class blocks(models.Model):
    block_num = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField()  

class votes(models.Model):
    voter = models.CharField(max_length=25)
    author = models.CharField(max_length=25)
    permlink = models.TextField()
    weight = models.IntegerField()
    value = models.FloatField(default=0)
    timestamp = models.DateTimeField(db_index=True)  

class transfers_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class transfers_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class transfers_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class transfers(models.Model):
    sender = models.CharField(max_length=25)
    receiver = models.CharField(max_length=25)
    amount = models.TextField()
    precision = models.TextField()
    nai = models.TextField()
    timestamp = models.DateTimeField(db_index=True) 

class claim_rewards_count_minute(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards_count_hour(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards_count_day(models.Model):
    count = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)

class claim_rewards(models.Model):
    account = models.CharField(max_length=25)
    reward_steem = models.TextField()
    reward_sbd = models.TextField()
    reward_vests = models.TextField()
    timestamp = models.DateTimeField(db_index=True) 