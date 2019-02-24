from rest_framework import serializers

class VotesCount(serializers.Serializer):
    count = serializers.IntegerField()
    timestamp = serializers.DateTimeField()