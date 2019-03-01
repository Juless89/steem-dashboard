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

class VotesSum(serializers.Serializer):
    analyses = serializers.CharField()
    resolution = serializers.CharField()
    data = serializers.CharField()
    timestamp = serializers.DateTimeField()