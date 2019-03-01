from rest_framework import serializers

class VotesCount(serializers.Serializer):
    count = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

class TransfersCount(serializers.Serializer):
    count = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

class ClaimRewardsCount(serializers.Serializer):
    count = serializers.IntegerField()
    timestamp = serializers.DateTimeField()